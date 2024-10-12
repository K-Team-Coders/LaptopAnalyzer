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
      const uuidToOrderMap = {};
      state.statements.forEach((statement) => {
        const uuids = JSON.parse(statement.uuids);
        const orders = JSON.parse(statement.order);
        uuids.forEach((uuid, index) => {
          uuidToOrderMap[uuid] = orders[index];
        });
      });

      const allUuids = state.statements.flatMap((statement) =>
        JSON.parse(statement.uuids)
      );
      const recentUuids = allUuids.slice(-7);

      return recentUuids
        .map((uuid) => ({
          uuid,
          order: uuidToOrderMap[uuid] || "Unknown",
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
        .get(`http://${process.env.VUE_APP_IP}:8000/result/uuids/`)
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
