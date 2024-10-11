<template>
  <aside class="">
    <div
      class="flex relative flex-col items-center w-64 h-full overflow-hidden text-gray-700 bg-gray-100 rounded shadow-lg shadow-[#c9c9c9]"
    >
      <div class="flex justify-center items-center w-full px-3 mt-4">
        <div class="flex flex-col mt-4 ml-2 text-[black]">
          <span class="text-5xl leading-[0.5] font-stengazeta tracking-[1px]"
            >Магистр</span
          >
          <span class="text-center text-[11px] font-stengazeta ml-[3px]"
            >интеллектуальный помощник</span
          >
        </div>
      </div>
      <div class="w-full px-2">
        <div class="flex flex-col w-full mt-3 border-t border-gray-300">
          <router-link
            v-for="service in services"
            :key="service.name"
            :to="service.route"
          >
            <SidebarCategory
              :category="service.category"
              :name="service.name"
              :classed="service.classed"
              :isActive="service.isActive"
              :collapsed="!sidebarStatus"
            />
          </router-link>
        </div>

        <div
          class="flex flex-col h-full w-full mt-2 mb-2 border-t border-gray-300"
        >
          <p class="pt-4 font-stengazeta text-lg text-center">
            Последние обращения
          </p>
          <router-link
            v-for="setting in statementNumber"
            :key="setting.name"
            :to="setting.route"
          >
            <SidebarCategory
              :category="setting.category"
              :name="setting.name"
              :classed="setting.classed"
              :isActive="setting.isActive"
            />
          </router-link>
        </div>
      </div>
    </div>
  </aside>
</template>
<script>
import SidebarCategory from "./SidebarCategory.vue";
export default {
  components: {
    SidebarCategory,
  },
  data() {
    return {
      statements: [
        { id: 1, category: "Заявка №976239", name: "history" },
        { id: 2, category: "Заявка №934676", name: "history" },
        { id: 3, category: "Заявка №345743", name: "history" },
        { id: 4, category: "Заявка №375893", name: "history" },
        { id: 5, category: "Заявка №239478", name: "history" },
        { id: 6, category: "Заявка №872387", name: "history" },
        { id: 7, category: "Заявка №238783", name: "history" },
        { id: 8, category: "Заявка №825878", name: "history" },
        { id: 9, category: "Заявка №478734", name: "history" },
      ],
    };
  },
  computed: {
    services() {
      return [
        {
          category: "Главная",
          name: "laptop",
          classed: "w-8 h-8 ml-1",
          route: "/",
          isActive: this.$route.path === "/",
        },
        {
          category: "История обращений",
          name: "news",
          classed: "w-8 h-8 ml-1",
          route: "/statement",
          isActive: this.$route.path === "/statement",
        },
        {
          category: "Статистика",
          name: "dashboard",
          classed: "w-8 h-8 ml-1 ",
          route: "/dashboard",
          isActive: this.$route.path === "/dashboard",
        },
      ];
    },
    statementNumber() {
      return this.statements.slice(0, 7).map((statement) => ({
        ...statement,
        classed: "w-8 h-8 ml-1",
        route: `/statement/${statement.id}`,
        isActive:
          this.$route && this.$route.path === `/statement/${statement.id}`,
      }));
    },
  },
};
</script>
