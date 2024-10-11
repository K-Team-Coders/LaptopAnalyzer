<template>
  <div class="h-full">
    <div v-if="this.isServiceLoading" class="p-2 h-full w-full">
      <div
        class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full flex justify-center items-center w-full"
      >
        <div class="flex flex-col items-center justify-center">
          <span class="loader"></span>
          <p class="pt-2 font-stengazeta text-xl">Идет загрузка...</p>
        </div>
      </div>
    </div>
    <div v-else-if="this.isServiceError" class="p-2 h-full">
      <div
        class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full"
      >
        <ErrorPage :status="error_info.code" :text="error_info.message" />
      </div>
    </div>

    <div v-else class="p-2 h-full">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import ErrorPage from "./ErrorPage.vue";

export default {
  components: {
    ErrorPage,
  },
  data() {
    return {
      error_info: {
        message: "Сервис не доступен! Проверьте подключение.",
        code: "ОШИБКА",
      },
    };
  },

  props: {
    isServiceError: {
      type: Boolean,
      require: true,
    },
    isServiceLoading: {
      type: Boolean,
      require: true,
    },
  },
};
</script>
<style scoped>
.loader {
  width: 148px;
  height: 148px;
  border-radius: 50%;
  display: inline-block;
  position: relative;
  border: 3px solid;
  border-color: #383838 #383838 transparent transparent;
  box-sizing: border-box;
  animation: rotation 1s linear infinite;
}
.loader::after,
.loader::before {
  content: "";
  box-sizing: border-box;
  position: absolute;
  left: 0;
  right: 0;
  top: 0;
  bottom: 0;
  margin: auto;
  border: 3px solid;
  border-color: transparent transparent #ff3d00 #ff3d00;
  width: 130px;
  height: 130px;
  border-radius: 50%;
  box-sizing: border-box;
  animation: rotationBack 0.5s linear infinite;
  transform-origin: center center;
}
.loader::before {
  width: 110px;
  height: 110px;
  border-color: #383838 #383838 transparent transparent;
  animation: rotation 1.5s linear infinite;
}

@keyframes rotation {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}
@keyframes rotationBack {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(-360deg);
  }
}
</style>
