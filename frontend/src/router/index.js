import { createRouter, createWebHistory } from "vue-router";
import HomePage from "@/views/HomePage.vue";
import History from "@/views/History.vue";
import HistoryItem from "@/views/HistoryItem.vue";

const routes = [
  {
    path: "/",
    name: "Home",
    component: HomePage,
  },
  {
    path: "/statement",
    name: "statement",
    component: History,
  },
  {
    path: "/statement/:id",
    name: "statement(id)",
    component: HistoryItem,
  },
  {
    path: "/dashboard",
    name: "dashboard",
    component: () => import("@/views/Dashboard.vue"),
  },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
