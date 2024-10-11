<template>
  <div class="flex items-center w-full justify-center text-neutral-600 duration-300 font-stengazeta p-2.5">
    <p class="text-lg">
      {{ localeDate }}
    </p>
    <p class="text-lg ml-1">
      {{ localeTime }}
    </p>
  </div>
</template>

<script>
export default {
  data: () => ({
    date: new Date(),
  }),

  computed: {
    localeDate() {
      return this.date.toLocaleDateString("ru-RU", {
        weekday: "long",
        month: "long",
        day: "numeric",
      });
    },
    localeTime() {
      return this.date.toLocaleTimeString("ru-RU", {
        hour: "2-digit",
        minute: "2-digit",
      });
    },
  },

  created() {
    this.intervalId = setInterval(() => (this.date = new Date()), 1000);
  },

  beforeDestroy() {
    if (this.intervalId) clearInterval(this.intervalId);
  },
};
</script>
