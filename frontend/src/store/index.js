import { createStore } from "vuex";
import axios from "axios";
export default createStore({
  state: {
    isOpenSidebar:
      localStorage.getItem("isOpenSidebar") !== null
        ? localStorage.getItem("isOpenSidebar") === "true"
        : true,
    statements: [
      {
        uuids: [
          "37d8b213-aedb-4830-9689-b441d752b514",
          "37d8b213-aedb-4830-9689-b441d752b545",
          "37d8b213-aedb-4830-9689-b441d752b421",
        ],
      },
    ],
  },
  getters: {
    isOpenSidebar: (state) => state.isOpenSidebar,
    statementNumber: (state) => {
      const allUuids = state.statements.flatMap((statement) => statement.uuids);
      const recentUuids = allUuids.slice(-7);
      return recentUuids
        .map((uuid) => ({
          uuid,
          classed: "w-8 h-8 ml-1",
          route: `/statement/${uuid}`,
        }))
        .reverse();
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
        .get(`http://${process.env.VUE_APP_IP}:8000/result/uuids`, {})
        .then((response) => {
          commit("setStatements", response.data);
          console.log("Statements fetched:", response.data);
        })
        .catch((error) => {
          console.error("Error fetching statements:", error);
        });
    },
  },
});
