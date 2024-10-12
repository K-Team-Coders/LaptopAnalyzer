import { createStore } from "vuex";
import axios from "axios";
export default createStore({
  state: {
    isOpenSidebar:
      localStorage.getItem("isOpenSidebar") !== null
        ? localStorage.getItem("isOpenSidebar") === "true"
        : true,
    statements: [],
  },
  getters: {
    isOpenSidebar: (state) => state.isOpenSidebar,
    statementNumber: (state) => {
      const statements = state.statements[0] || { uuids: [], order: [] };
      const showLast = 6;
      const start = Math.max(statements.uuids.length - showLast, 0);

      return statements.uuids.slice(start).map((uuid, index) => ({
        uuid: uuid,
        order: statements.order[start + index],
        route: `/statement/${uuid}`,
      }));
    },
    allStatements: (state) => state.statements,
  },
  mutations: {
    toggleSidebar(state) {
      state.isOpenSidebar = !state.isOpenSidebar;
      localStorage.setItem("isOpenSidebar", state.isOpenSidebar);
    },
    setStatements(state, statements) {
      state.statements = statements;
    },
  },
  actions: {
    toggleSidebar({ commit }) {
      commit("toggleSidebar");
    },

    fetchStatements({ commit }) {
      axios
        .get(`http://${process.env.VUE_APP_IP}:8000/result/uuids/`)
        .then((response) => {
          let sum = [
            {
              uuids: JSON.parse(response.data.uuids),
              order: JSON.parse(response.data.order),
            },
          ];
          console.log(sum);
          commit("setStatements", sum);
        })
        .catch((error) => {
          console.error("Error fetching statements:", error);
        });
    },
  },
});
