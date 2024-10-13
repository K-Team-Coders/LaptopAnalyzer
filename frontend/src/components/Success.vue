<template>
  <transition
    enter-active-class="transition ease-in-out duration-300 transform"
    enter-from-class="translate-x-full"
    enter-to-class="translate-x-0"
    leave-active-class="transition ease-in-out duration-300 transform"
    leave-from-class="translate-x-0"
    leave-to-class="translate-x-full"
  >
    <div
      class="fixed top-0 right-0 bg-teal-100 border-t-4 border-teal-500 rounded-b text-teal-900 px-8 py-5 shadow-md"
      role="alert"
      v-if="state"
    >
      <div class="flex items-center">
        <div class="py-1">
          <svg
            class="fill-current h-6 w-6 text-teal-500 mr-4"
            xmlns="http://www.w3.org/2000/svg"
            viewBox="0 0 20 20"
          >
            <path
              d="M2.93 17.07A10 10 0 1 1 17.07 2.93 10 10 0 0 1 2.93 17.07zm12.73-1.41A8 8 0 1 0 4.34 4.34a8 8 0 0 0 11.32 11.32zM9 11V9h2v6H9v-4zm0-6h2v2H9V5z"
            />
          </svg>
        </div>
        <div>
          <p class="font-bold">Сохранения изменены</p>
        </div>
      </div>
    </div>
  </transition>
</template>
<script>
export default {
  props: {
    state: {
      type: Boolean,
      default: false,
    },
  },
};
</script>
