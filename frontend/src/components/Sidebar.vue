<template>
  <aside class="">
    <div
      class="flex relative flex-col items-center w-64 h-full overflow-hidden text-gray-700 bg-gray-100 rounded shadow-lg shadow-[#c9c9c9]"
    >
      <div class="flex justify-center items-center w-full px-3 mt-4">
        <img class="w-12 h-12" src="@/img/logo.png" />
        <div class="flex flex-col justify-start mt-4 ml-2 text-[black]">
          <p class="text-5xl leading-[0.5] font-stengazeta">Магистр</p>
          <p class="text-[11px] font-stengazeta">интеллектуальный помощник</p>
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
            Последние заключения
          </p>
          <router-link
            v-for="setting in statementNumber"
            :key="setting.category"
            :to="setting.route"
            custom
            v-slot="{ navigate, isActive, isExactActive }"
          >
            <SidebarCategory
              :category="setting.category"
              name="history"
              :classed="setting.classed"
              :isActive="isActive || isExactActive"
              @click.native="navigate"
            />
          </router-link>
        </div>
      </div>
    </div>
  </aside>
</template>
<script>
import SidebarCategory from "./SidebarCategory.vue";
import { mapGetters } from "vuex";
export default {
  components: {
    SidebarCategory,
  },
  data() {
    return {
      statements: [],
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
          category: "История заключений",
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
        {
          category: "Дообучение",
          name: "settings",
          classed: "w-8 h-8 ml-1 ",
          route: "/training",
          isActive: this.$route.path === "/training",
        },
      ];
    },
    ...mapGetters(["statementNumber"]),
  },
  methods: {
    getLastStatements() {
      axios
        .get(`http://${process.env.VUE_APP_IP}/statement`)
        .then((response) => {
          this.statements = response.data;
        })
        .catch((error) => {
          console.error("Error fetching statements:", error);
        });
    },
  },
  created() {
    this.$store.dispatch("fetchStatements");
  },
};
</script>
