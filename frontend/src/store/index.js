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
      return state.statements
        .slice(Math.max(state.statements.length - 7, 0))
        .map((statement) => ({
          ...statement,
          classed: "w-8 h-8 ml-1",
          route: `/statement/${statement.id}`,
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
        .get(`http://${process.env.VUE_APP_IP}/statement`)
        .then((response) => {
          commit("setStatements", response.data);
        })
        .catch((error) => {
          console.error("Error fetching statements:", error);
        });
    },
  },
});
