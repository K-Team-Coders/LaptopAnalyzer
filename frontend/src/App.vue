<template>
  <div class="flex w-full h-screen custom-scrollbar">
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
  computed: {
    ...mapGetters(["isOpenSidebar"]),
  },
  methods: {
    ...mapActions(["toggleSidebar"]),
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
