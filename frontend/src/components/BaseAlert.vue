<template>
  <transition
    enter-active-class="transition ease-in-out duration-300 transform"
    enter-from-class="translate-x-full"
    enter-to-class="translate-x-0"
    leave-active-class="transition ease-in-out duration-300 transform"
    leave-from-class="translate-x-0"
    leave-to-class="translate-x-full"
  >
    <div v-if="state" class="alert">
      <div
        class="alert__container"
        :style="{
          'background-color': style[color].bg,
          'border-color': style[color].text,
          color: style[color].text,
        }"
        role="alert"
      >
        <BaseIcon name="x" class="alert__close" @click="$emit('close')" />
        <div class="alert__title">{{ title }}</div>
        <div class="alert__text" v-html="text"></div>
      </div>
    </div>
  </transition>
</template>
<script>
import BaseIcon from "./BaseIcon.vue";

export default {
  components: { BaseIcon },
  
  data() {
    return {
      style: {
        red: {
          bg: "#febaba",
          text: "#b91c1c",
        },
        blue: {
          bg: "#bfdbfe",
          text: "#3b82f6",
        },
        green: {
          bg: "#bbf7d0",
          text: "#15803d",
        },
        yellow: {
          bg: "#ffc10c",
          text: "#2b200b",
        },
      },
    };
  },
  methods: {},
  props: {
    color: {
      Object: String,
      require: true,
    },
    state: {
      Object: Boolean,
      default: false,
    },
    title: {
      Object: String,
      require: true,
    },
    text: {
      Object: String,
      require: true,
    },
  },
};
</script>

<style scoped>
.alert {
  position: fixed;
  right: 0;
  bottom: 0;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.alert__container {
  border-left-width: 4px;
  padding: 1rem;
  width: 24rem;
}

.alert__close {
  position: absolute;
  width: 1.5rem;
  height: 1.5rem;
  right: 1rem;
  top: 1rem;
}

.alert__close:hover {
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  opacity: 0.5;
}

.alert__title {
  font-size: 1.25rem;
  line-height: 1.75rem;
  font-weight: 700;
}

.alert_text {
  font-size: 1.125rem;
  line-height: 1.75rem;
}
</style>
