<template>
  <div class="h-full p-2">
    <div
      class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full flex flex-col"
    >
      <div
        class="flex items-center h-12 m-2.5 rounded-[5px] border border-neutral-400"
      >
        <input
          ref="input"
          v-model="this.queryMessage"
          class="w-full p-2.5 placeholder:text-neutral-400 bg-transparent outline-none"
          type="text"
          placeholder="Введите номер заключения..."
        />
        <button title="Поиск" class="mr-3">
          <img class="w-5 h-5" src="@/img/search.png" />
        </button>
      </div>
      <div class="relative h-full w-full">
        <div
          v-if="isLoading"
          class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex flex-col justify-center items-center"
        >
          <span class="loader"></span>
          <p class="text-black pt-2 font-stengazeta text-sm">
            Идет загрузка заключений...
          </p>
        </div>
        <div
          class="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 flex flex-col justify-center items-center"
          v-else-if="this.items.length == 0"
        >
          <p class="text-neutral-200 text-3xl pt-2 font-stengazeta text-center">
            Заключений нет
          </p>
        </div>
        <div v-else class="flex flex-wrap gap-2 w-auto px-2.5">
          <router-link
            v-for="item in filteredItems"
            :key="item.uuid"
            :to="item.route"
            class="p-2 border-2 border-neutral-400 h-auto w-40 rounded-[5px] cursor-pointer hover:border-yellow-500 duration-100"
          >
            <div>
              <p class="text-center font-semibold">Заключение</p>
              <p class="text-center">№ {{ item.order }}</p>
            </div>
          </router-link>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
import { mapGetters } from "vuex";
export default {
  data() {
    return {
      queryMessage: "",
      isLoading: false,
    };
  },
  methods: {},

  computed: {
    ...mapGetters(["allStatements"]),
    items() {
      return this.allStatements;
    },
    filteredItems() {
      return this.allStatements.filter((item) => {
        return this.queryMessage
          .toLowerCase()
          .split(" ")
          .every((v) => item.order.toLowerCase().includes(v));
      });
    },
  },
  mounted() {
    this.$refs.input.focus();
    this.isLoading = false;
  },
};
</script>
<style scoped>
.loader {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: inline-block;
  border-top: 3px solid #000000;
  border-right: 3px solid transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
</style>
