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
          class="flex flex-col flex-grow h-full w-full mt-2 mb-2 border-t border-gray-300"
        >
          <p class="pt-4 font-stengazeta text-lg text-center">Последние обращения</p>
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
        { id: 1, category: "Обращение №1", name: "history" },
        { id: 2, category: "Обращение №2", name: "history" },
        { id: 3, category: "Обращение №3", name: "history" },
        { id: 4, category: "Обращение №4", name: "history" },
        { id: 5, category: "Обращение №5", name: "history" },
        { id: 6, category: "Обращение №6", name: "history" },
        { id: 7, category: "Обращение №7", name: "history" },
        { id: 8, category: "Обращение №8", name: "history" },
        { id: 9, category: "Обращение №9", name: "history" },
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
      ];
    },
    statementNumber() {
      return this.statements.slice(0, 8).map((statement) => ({
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
