<template>
  <a
    class="flex items-center w-full h-12 px-3 mt-2 rounded hover:bg-gray-300 duration-100 cursor-pointer"
    :class="{
      'bg-gray-300': isActive,
    }"
  >
    <span class="w-6 h-6" v-html="iconSvg"></span>
    <span class="ml-2 text-sm font-medium">{{ category }}</span>
  </a>
</template>
<script>
import icons from "../icons";

export default {
  props: {
    category: {
      type: String,
      required: true,
    },
    isActive: {
      type: Boolean,
      default: false,
    },
    name: {
      type: String,
      required: true,
    },
    classed: {
      type: String,
      default: "",
    },
    collapsed: {
      type: Boolean,
      default: false,
    },
  },
  computed: {
    iconSvg() {
      return icons[this.name] || icons["default"]; // Предусмотрите дефолтную иконку
    },
  },
};
</script>
