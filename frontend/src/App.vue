<template>
  <div class="flex w-full h-screen custom-scrollbar">
    <div v-if="isLearning">
      <div
        class="h-[10px] fixed bg-red-500 z-[1000] rounded"
        :style="{ width: progressBarWidth }"
      ></div>
    </div>
    <transition
      enter-active-class="transition ease-in-out duration-50 transform"
      enter-from-class="-translate-x-full "
      enter-to-class="translate-x-0"
      leave-active-class=""
      leave-from-class="translate-x-0"
      leave-to-class="-translate-x-full"
    >
      <Sidebar v-if="isOpenSidebar" />
    </transition>

    <ButtonStateSidebar />
    <main class="w-full flex-grow">
      <router-view />
    </main>
  </div>
</template>
<script>
import ButtonStateSidebar from "./components/ButtonStateSidebar.vue";
import Sidebar from "./components/Sidebar.vue";

import { mapGetters, mapActions } from "vuex";
export default {
  components: {
    ButtonStateSidebar,
    Sidebar,
  },
  data() {
    return {
      duration: 1000000, // Продолжительность анимации в миллисекундах (10 секунд)
      elapsedTime: 0, // Прошедшее время с начала анимации
      interval: null, // Хранение ссылки на setInterval
    };
  },
  computed: {
    ...mapGetters(["isOpenSidebar"]),
    ...mapGetters(["isLearning"]),
    progressBarWidth() {
      const progress = (this.elapsedTime / this.duration) * 100;
      return `${progress}%`; // Ширина в процентах
    },
  },
  methods: {
    ...mapActions(["toggleSidebar"]),
    ...mapActions(["fetchStatements"]),
    ...mapActions(["setLearning"]),
    startProgressBar() {
      this.resetProgressBar();
      this.interval = setInterval(() => {
        this.elapsedTime += 5; // Увеличиваем на 10 мс каждый интервал
        if (this.elapsedTime >= this.duration) {
          this.completeProgressBar();
        }
      }, 10);
    },
    resetProgressBar() {
      if (this.interval) {
        clearInterval(this.interval); // Очистка существующего интервала, если он есть
      }
      this.elapsedTime = 0; // Сброс прошедшего времени
    },
    completeProgressBar() {
      this.elapsedTime = this.duration; // Убедимся, что время не превышает длительность
      clearInterval(this.interval); // Очистка интервала после завершения
      this.setLearning(false); // Сброс isLearning в Vuex
    },
  },
  watch: {
    isLearning(newVal) {
      if (newVal) {
        this.startProgressBar(); // Запуск анимации при изменении isLearning на true
      } else {
        this.resetProgressBar(); // Сброс прогресса, если isLearning стал false
      }
    },
  },
  mounted() {
    this.fetchStatements();
  },
};
</script>
<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 10px;
}

.custom-scrollbar::-webkit-scrollbar-track {
  background: transparent;
}

.custom-scrollbar::-webkit-scrollbar-thumb {
  background-color: rgb(115, 115, 115);
  border-radius: 10px;
}

/* Для Firefox */
.custom-scrollbar {
  scrollbar-width: thin;
  scrollbar-color: rgb(115, 115, 115) transparent;
}
</style>
