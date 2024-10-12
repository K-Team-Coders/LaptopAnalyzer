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
        <div class="text-2xl text-center w-full font-stengazeta px-4 py-4">
          <span class="text-3xl"> Техническое заключение </span><br />от
          <span class="text-red-500"> {{ this.creationDate }} </span>
          № <span class="text-red-500"> {{ this.conclusionNumber }} </span>
        </div>
        <div class="flex w-full">
          <div class="w-8/12 p-2">
            <div class="flex items-center justify-center w-full">
              <label
                for="dropzone-file"
                class="flex flex-col items-center justify-center w-full h-96 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
              >
                <div
                  class="flex flex-col items-center justify-center pt-5 pb-6"
                >
                  <svg
                    class="w-8 h-8 mb-4 text-gray-400"
                    aria-hidden="true"
                    xmlns="http://www.w3.org/2000/svg"
                    fill="none"
                    viewBox="0 0 20 16"
                  >
                    <path
                      stroke="currentColor"
                      stroke-linecap="round"
                      stroke-linejoin="round"
                      stroke-width="2"
                      d="M13 13h3a3 3 0 0 0 0-6h-.025A5.56 5.56 0 0 0 16 6.5 5.5 5.5 0 0 0 5.207 5.021C5.137 5.017 5.071 5 5 5a4 4 0 0 0 0 8h2.167M10 15V6m0 0L8 8m2-2 2 2"
                    />
                  </svg>
                  <p class="mb-2 text-gray-700 text-md">
                    <span class="font-semibold">Нажмите чтобы загрузить</span>
                    или перенесите файлы
                  </p>
                  <p class="text-xs text-gray-700 text-md">(PNG, JPG)</p>
                </div>
                <input
                  id="dropzone-file"
                  type="file"
                  class="hidden"
                  accept="image/png, image/jpeg"
                />
              </label>
            </div>
          </div>
          <div class="w-4/12 h-full p-2 flex flex-col gap-2">
            <p class="font-bold text-xl text-center">Информация об изделии</p>
            <label class="block">
              <span class="block text-sm font-medium text-gray-700">Фирма</span>
              <input
                v-model="this.firmName"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
            <label class="block">
              <span class="block text-sm font-medium text-gray-700"
                >Модель</span
              >
              <input
                v-model="this.modelName"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
            <label class="block">
              <span class="block text-sm font-medium text-gray-700"
                >Дата ввода в эксплуатацию</span
              >
              <input
                v-model="this.expluatationDate"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
            <div>
              <label class="block">
                <span class="block text-sm font-medium text-gray-700"
                  >Серийный номер</span
                >
                <input
                  v-model="this.serialNumber"
                  type="text"
                  class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                />
              </label>
            </div>
          </div>
        </div>
        <div class="w-full">
          <div>
            <p class="font-bold text-xl px-2 pt-2">Информация об заявителе</p>
          </div>
          <div class="w-full p-2 flex gap-4">
            <label class="block w-1/3">
              <span class="block text-sm font-medium text-gray-700"
                >ФИО заявителя</span
              >
              <input
                v-model="this.clientName"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
            <label class="block w-1/3">
              <span class="block text-sm font-medium text-gray-700"
                >Номер телефона</span
              >
              <input
                v-model="this.clientPhone"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
            <label class="block w-1/3">
              <span class="block text-sm font-medium text-gray-700">Адрес</span>
              <input
                v-model="this.clientAddress"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
          </div>
          <div>
            <label class="block w-full px-2 pt-1">
              <span class="block text-sm font-medium text-gray-700"
                >Указанные неисправности (со слов заявителя)</span
              >
              <textarea
                v-model="this.clientDefects"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              ></textarea>
            </label>
          </div>
        </div>
        <div class="w-full pt-2">
          <div>
            <p class="font-bold text-xl px-2 pt-2">Информация об исполнителе</p>
          </div>
          <div class="w-full p-2 flex gap-4">
            <label class="block w-1/3">
              <span class="block text-sm font-medium text-gray-700"
                >ФИО исполнителя</span
              >
              <input
                v-model="this.executorName"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
            <label class="block w-1/3">
              <span class="block text-sm font-medium text-gray-700"
                >Номер телефона</span
              >
              <input
                v-model="this.executorPhone"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
            <label class="block w-1/3">
              <span class="block text-sm font-medium text-gray-700"
                >Адрес сервисного центра</span
              >
              <input
                v-model="this.serviceCenterAddress"
                type="text"
                class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
              />
            </label>
          </div>
        </div>

        <div class="p-2">
          <h3 class="text-lg font-medium text-gray-900">
            Техническое заключение
          </h3>
          <textarea
            v-model="this.conclusionText"
            class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm min-h-32"
          >
          </textarea>
        </div>
        <div class="flex justify-end py-2">
          <button
            type="button"
            class="text-white bg-blue-600 hover:bg-blue-700 focus:ring-4 focus:ring-blue-300 font-medium rounded-lg text-sm px-8 py-2.5 me-2 mb-2 focus:outline-none"
          >
            Сохранить изменения
          </button>
        </div>
      </div>
    </div>
  </div>
</template>
<script>
export default {
  data() {
    return {
      id: null,
      creationDate: "11.10.2024",
      conclusionNumber: "0000001",
      firmName: "",
      modelName: "",
      expluatationDate: "",
      serialNumber: "",
      clientName: "",
      clientPhone: "",
      clientAddress: "",
      clientDefects: "",
      executorName: "",
      executorPhone: "",
      serviceCenterAddress: "",
      conclusionText: "",
      fileArr: [],

      isServiceLoading: false,
    };
  },
  mounted() {
    this.isServiceLoading = true;
    setTimeout(() => {
      this.isServiceLoading = false;
    }, 1000);
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
