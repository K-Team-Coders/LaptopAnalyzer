<template>
  <div class="h-full w-full p-2">
    <div
      class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full flex flex-col flex-grow overflow-y-auto"
    >
      <div
        v-if="this.isServiceLoading"
        class="h-full w-full flex flex-col justify-center items-center"
      >
        <span class="loader"></span>
        <p class="text-black pt-2 font-stengazeta text-sm">
          Идет загрузка формы...
        </p>
      </div>
      <div v-else class="flex flex-col">
        <form @submit.prevent="setLearning">
          <div class="flex w-full justify-center pt-8">
            <div class="w-6/12 h-full p-2 flex flex-col gap-2">
              <p class="font-bold text-xl text-center">Гиперпараметры модели</p>
              <label class="block">
                <span class="block text-sm font-medium text-gray-700"
                  >Тип модели</span
                >
                <select
                  v-model="selectedModel"
                  placeholder="Выберите модель"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.firmName
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                >
                  <option v-for="(type, index) in modelType" :key="index">
                    {{ type.legend }}
                  </option>
                </select>
                <span
                  v-if="this.errors.selectedModel"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.selectedModel }}
                </span>
              </label>
              <label class="block">
                <span class="block text-sm font-medium text-gray-700"
                  >Количество эпох</span
                >
                <input
                  v-model="this.epochs"
                  type="number"
                  min="1"
                  pattern="\d+"
                  placeholder="Введите количество эпох"
                  step="1"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.epochs
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span v-if="this.errors.epochs" class="text-red-500 text-sm">
                  {{ this.errors.epochs }}
                </span>
              </label>
              <label class="block">
                <span class="block text-sm font-medium text-gray-700"
                  >Размер входного окна (batch size)</span
                >
                <input
                  v-model="this.batchSize"
                  type="number"
                  min="1"
                  pattern="\d+"
                  placeholder="Введите количество эпох"
                  step="1"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.batchSize
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span v-if="this.errors.batchSize" class="text-red-500 text-sm">
                  {{ this.errors.batchSize }}
                </span>
              </label>
              <div>
                <label class="block">
                  <span class="block text-sm font-medium text-gray-700"
                    >Период сохранения модели, эпохи</span
                  >
                  <input
                    v-model="this.savePeriod"
                    type="number"
                    min="1"
                    pattern="\d+"
                    placeholder="Введите количество эпох"
                    step="1"
                    :class="[
                      'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                      this.errors.savePeriod
                        ? 'border-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                    ]"
                  />
                </label>
                <span
                  v-if="this.errors.savePeriod"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.savePeriod }}
                </span>
              </div>
              <div>
                <label class="block">
                  <span class="block text-sm font-medium text-gray-700"
                    >Скорость обучения</span
                  >
                  <input
                    v-model="this.learningRate"
                    type="number"
                    min="0.001"
                    max="1"
                    placeholder="Введите количество эпох"
                    step="0.1"
                    :class="[
                      'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                      this.errors.learningRate
                        ? 'border-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                    ]"
                  />
                </label>
                <span
                  v-if="this.errors.learningRate"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.learningRate }}
                </span>
              </div>
              <div>
                <label class="block">
                  <span class="block text-sm font-medium text-gray-700"
                    >Оптимизаторы</span
                  >
                  <select
                    v-model="selectedOptimizer"
                    placeholder="Выберите модель"
                    :class="[
                      'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                      this.errors.firmName
                        ? 'border-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                    ]"
                  >
                    <option
                      v-for="(optimizer, index) in optimizers"
                      :key="index"
                    >
                      {{ optimizer }}
                    </option>
                  </select>
                  <span
                    v-if="this.errors.selectedModel"
                    class="text-red-500 text-sm"
                  >
                    {{ this.errors.selectedModel }}
                  </span>
                </label>
              </div>
            </div>
          </div>
          <div class="flex justify-center pt-4">
            <button
              v-if="!isLearning"
              type="submit"
              class="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-11 py-2.5 duration-100 me-2 mb-2 focus:outline-none"
            >
              НАЧАТЬ ОБУЧЕНИЕ
            </button>
            <button
              v-else
              type="submit"
              class="text-white bg-blue-700 hover:bg-blue-800 focus:outline-none font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center"
            >
              <svg
                aria-hidden="true"
                role="status"
                class="inline w-4 h-4 me-3 text-white animate-spin"
                viewBox="0 0 100 101"
                fill="none"
                xmlns="http://www.w3.org/2000/svg"
              >
                <path
                  d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z"
                  fill="#E5E7EB"
                />
                <path
                  d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z"
                  fill="currentColor"
                />
              </svg>
              Обучение
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>
<script>
import axios from "axios";
import { mapActions, mapGetters } from "vuex";
export default {
  data() {
    return {
      id: null,
      epochs: 100,
      batchSize: 16,
      savePeriod: 15,
      fileArr: [],
      learningRate: 0.501,
      selectedModel: "Точная",
      modelType: [
        {
          legend: "Быстрая",
          name: "yolov11.pt",
        },
        {
          legend: "Оптимальная",
          name: "yolov11.pt",
        },
        {
          legend: "Точная",
          name: "yolov11.pt",
        },
      ],
      optimizers: ["SGD", "Adam", "AdamW", "NAdam", "RAdam", "RMSProp", "auto"],
      selectedOptimizer: "auto",

      isServiceLoading: false,

      errors: {},
      activeIndex: 0,

      formDates: {
        fileArr: [],
      },
      isSaving: false,
    };
  },
  mounted() {
    this.isServiceLoading = true;
    setTimeout(() => {
      this.isServiceLoading = false;
    }, 1000);
  },
  methods: {
    ...mapActions(["setLearning"]),
  },
  computed: {
    ...mapGetters(["isLearning"]),
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
