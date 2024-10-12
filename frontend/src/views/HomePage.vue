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
      <div
        v-else-if="this.isSending"
        class="h-full w-full flex flex-col justify-center items-center"
      >
        <span class="loader"></span>
        <p class="text-black pt-2 font-stengazeta text-sm">
          Происходит анализ...
        </p>
      </div>
      <div v-else class="h-full w-full flex flex-col">
        <form @submit.prevent="handleSubmit">
          <p class="text-2xl text-center w-full font-stengazeta px-4 py-4">
            <span class="text-3xl">Создание технического заключения </span>
          </p>
          <div class="flex w-full">
            <div class="w-8/12 p-2">
              <div
                v-if="fileArr.length === 0"
                class="flex flex-col items-center justify-center w-full"
              >
                <label
                  for="dropzone-file"
                  class="flex flex-col items-center justify-center w-full h-96 border-2 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.files
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
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
                    ref="dropzoneInput"
                    type="file"
                    class="hidden"
                    accept="image/png, image/jpeg"
                    multiple
                    @change="handleFiles"
                  />
                </label>
                <span v-if="this.errors.files" class="text-red-500 text-sm">
                  {{ this.errors.files }}
                </span>
              </div>
              <div
                v-else
                class="w-full relative flex flex-col border-2 border-gray-300 border-dashed rounded-lg bg-gray-50 py-2 px-4"
              >
                <div class="flex items-center justify-center w-full h-96">
                  <div class="flex justify-center w-full">
                    <div class="flex justify-center w-full">
                      <img
                        :src="fileArr[this.activeIndex]"
                        class="w-auto h-96 rounded-lg"
                        alt="active image"
                      />
                    </div>
                  </div>
                </div>
                <input
                  id="dropzone-file"
                  ref="dropzoneInput"
                  type="file"
                  class="hidden"
                  accept="image/png, image/jpeg"
                  multiple
                  @change="handleFiles"
                />
                <template class="w-full flex items-center justify-center">
                  <div class="mt-4 mr-2">
                    <button
                      @click="openFileDialog"
                      class="w-8 h-8 bg-green-500 rounded-full"
                    >
                      <svg
                        viewBox="0 0 24 24"
                        fill="none"
                        xmlns="http://www.w3.org/2000/svg"
                      >
                        <path
                          d="M4 12H20M12 4V20"
                          stroke="#ffffff"
                          stroke-width="2"
                          stroke-linecap="round"
                          stroke-linejoin="round"
                        />
                      </svg>
                    </button>
                  </div>
                  <div
                    class="flex items-center space-x-2 mt-4 overflow-x-auto max-w-[40vw] mx-auto custom-scroll"
                  >
                    <div
                      v-for="(image, index) in fileArr"
                      :key="index"
                      class="w-24 h-24 border-2 rounded-md overflow-hidden cursor-pointer flex-shrink-0 relative"
                      :class="{
                        'border-yellow-500': index == this.activeIndex,
                      }"
                      @click="setActive(index)"
                    >
                      <img :src="image" class="w-full h-full object-cover" />
                      <button
                        @click.stop="removeFile(index)"
                        type="button"
                        class="absolute top-1 right-1 bg-red-600 hover:bg-red-700 duration-75 p-1 w-6 h-6 rounded-full"
                      >
                        <svg
                          fill="#ffffff"
                          viewBox="-3.5 0 19 19"
                          xmlns="http://www.w3.org/2000/svg"
                          class="cf-icon-svg"
                        >
                          <path
                            d="M11.383 13.644A1.03 1.03 0 0 1 9.928 15.1L6 11.172 2.072 15.1a1.03 1.03 0 1 1-1.455-1.456l3.928-3.928L.617 5.79a1.03 1.03 0 1 1 1.455-1.456L6 8.261l3.928-3.928a1.03 1.03 0 0 1 1.455 1.456L7.455 9.716z"
                          />
                        </svg>
                      </button>
                    </div></div
                ></template>
              </div>
            </div>
            <div class="w-4/12 h-full p-2 flex flex-col gap-2">
              <p class="font-bold text-xl text-center">Информация об изделии</p>
              <label class="block">
                <span class="block text-sm font-medium text-gray-700"
                  >Фирма</span
                >
                <input
                  type="text"
                  v-model="this.firmName"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.firmName
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span v-if="this.errors.firmName" class="text-red-500 text-sm">
                  {{ this.errors.firmName }}
                </span>
              </label>
              <label class="block">
                <span class="block text-sm font-medium text-gray-700"
                  >Модель</span
                >
                <input
                  v-model="this.modelName"
                  type="text"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.modelName
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span v-if="this.errors.modelName" class="text-red-500 text-sm">
                  {{ this.errors.modelName }}
                </span>
              </label>
              <label class="block">
                <span class="block text-sm font-medium text-gray-700"
                  >Дата ввода в эксплуатацию</span
                >
                <input
                  v-model="this.expluatationDate"
                  type="date"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.expluatationDate
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span
                  v-if="this.errors.expluatationDate"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.expluatationDate }}
                </span>
              </label>
              <div>
                <label class="block">
                  <span class="block text-sm font-medium text-gray-700"
                    >Серийный номер</span
                  >
                  <input
                    v-model="this.serialNumber"
                    type="text"
                    :class="[
                      'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                      this.errors.serialNumber
                        ? 'border-red-500 focus:border-red-500'
                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                    ]"
                  />
                </label>
                <span
                  v-if="this.errors.serialNumber"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.serialNumber }}
                </span>
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
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.clientName
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span
                  v-if="this.errors.clientName"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.clientName }}
                </span>
              </label>
              <label class="block w-1/3">
                <span class="block text-sm font-medium text-gray-700"
                  >Номер телефона</span
                >
                <input
                  v-model="this.clientPhone"
                  type="tel"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.clientPhone
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                  placeholder="8-xxx-xxx-xx-xx"
                  pattern="[0-9]*"
                  inputmode="numeric"
                  @input="onInput($event)"
                />
                <span
                  v-if="this.errors.clientPhone"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.clientPhone }}
                </span>
              </label>
              <label class="block w-1/3">
                <span class="block text-sm font-medium text-gray-700"
                  >Адрес</span
                >
                <input
                  v-model="this.clientAddress"
                  type="text"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.clientAddress
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span
                  v-if="this.errors.clientAddress"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.clientAddress }}
                </span>
              </label>
            </div>
            <div>
              <label class="block w-full px-2 pt-1">
                <span class="block text-sm font-medium text-gray-700"
                  >Указанные неисправности (со слов заявителя)</span
                >
                <textarea
                  v-model="this.clientDefects"
                  class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
                ></textarea>
              </label>
            </div>
          </div>
          <div class="w-full pt-2">
            <div>
              <p class="font-bold text-xl px-2 pt-2">
                Информация об исполнителе
              </p>
            </div>
            <div class="w-full p-2 flex gap-4">
              <label class="block w-1/3">
                <span class="block text-sm font-medium text-gray-700"
                  >ФИО исполнителя</span
                >
                <input
                  v-model="this.executorName"
                  type="text"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.executorName
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span
                  v-if="this.errors.executorName"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.executorName }}
                </span>
              </label>
              <label class="block w-1/3">
                <span class="block text-sm font-medium text-gray-700"
                  >Номер телефона</span
                >
                <input
                  type="tel"
                  v-model="this.executorPhone"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.executorPhone
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                  placeholder="8-xxx-xxx-xx-xx"
                  pattern="[0-9]*"
                  inputmode="numeric"
                  @input="onInput($event)"
                />
                <span
                  v-if="this.errors.executorPhone"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.executorPhone }}
                </span>
              </label>
              <label class="block w-1/3">
                <span class="block text-sm font-medium text-gray-700"
                  >Адрес сервисного центра</span
                >
                <input
                  v-model="this.serviceCenterAddress"
                  type="text"
                  :class="[
                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                    this.errors.serviceCenterAddress
                      ? 'border-red-500 focus:border-red-500'
                      : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                  ]"
                />
                <span
                  v-if="this.errors.serviceCenterAddress"
                  class="text-red-500 text-sm"
                >
                  {{ this.errors.serviceCenterAddress }}
                </span>
              </label>
            </div>
          </div>
          <div class="flex justify-end py-2">
            <button
              type="submit"
              class="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-8 py-2.5 me-2 mb-2 focus:outline-none"
            >
              Отправить на анализ
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      firmName: "",
      modelName: "",
      creationDate: "",
      expluatationDate: "",
      serialNumber: "",
      clientName: "",
      clientPhone: "",
      clientAddress: "",
      clientDefects: "",
      executorName: "",
      executorPhone: "",
      serviceCenterAddress: "",
      fileArr: [],

      isServiceLoading: false,
      errors: {},
      activeIndex: 0,

      formDates: {
        fileArr: [],
      },
      isSending: false,
    };
  },
  mounted() {
    this.isServiceLoading = true;
    setTimeout(() => {
      this.isServiceLoading = false;
    }, 1000);
  },

  methods: {
    handleFiles(event) {
      const files = event.target.files;

      for (let i = 0; i < files.length; i++) {
        const file = files[i];
        if (file.type.startsWith("image/")) {
          const isDuplicate = this.formDates.fileArr.some(
            (existingFile) => existingFile.name === file.name
          );

          if (!isDuplicate) {
            const reader = new FileReader();
            reader.onload = (e) => {
              this.fileArr.push(e.target.result);
            };
            reader.readAsDataURL(file);
            this.formDates.fileArr.push(file);
          }
        }
      }
      // Очистка input после обработки файлов
      event.target.value = "";
    },
    async handleSubmit(event) {
      event.preventDefault();
      this.errors = {};
      if (!this.fileArr.length) {
        this.errors.files = "Поле обязательно для заполнения.";
      }

      if (!this.firmName) {
        this.errors.firmName = "Поле обязательно для заполнения.";
      }
      if (!this.modelName) {
        this.errors.modelName = "Поле обязательно для заполнения.";
      }
      if (!this.expluatationDate) {
        this.errors.expluatationDate = "Поле обязательно для заполнения.";
      }
      if (!this.serialNumber) {
        this.errors.serialNumber = "Поле обязательно для заполнения.";
      }
      if (!this.clientName) {
        this.errors.clientName = "Поле обязательно для заполнения.";
      }
      if (!this.clientPhone) {
        this.errors.clientPhone = "Поле обязательно для заполнения.";
      }
      if (!this.clientAddress) {
        this.errors.clientAddress = "Поле обязательно для заполнения.";
      }
      if (!this.executorName) {
        this.errors.executorName = "Поле обязательно для заполнения.";
      }
      if (!this.executorPhone) {
        this.errors.executorPhone = "Поле обязательно для заполнения.";
      }
      if (!this.serviceCenterAddress) {
        this.errors.serviceCenterAddress = "Поле обязательно для заполнения.";
      }

      if (Object.keys(this.errors).length > 0) {
        return;
      }
      const formData = new FormData(event.target);
      this.getDate();
      formData.append("firmName", this.firmName);
      formData.append("modelName", this.modelName);
      formData.append("creationDate", this.creationDate);
      formData.append("expluatationDate", this.expluatationDate);
      formData.append("serialNumber", this.serialNumber);
      formData.append("clientName", this.clientName);
      formData.append("clientPhone", this.clientPhone);
      formData.append("clientAddress", this.clientAddress);
      formData.append("clientDefects", this.clientDefects);
      formData.append("executorName", this.executorName);
      formData.append("executorPhone", this.executorPhone);
      formData.append("serviceCenterAddress", this.serviceCenterAddress);

      this.formDates.fileArr.forEach((file, index) => {
        formData.append(`file${index}`, file);
      });
      try {
        this.isSending = true;
        const response = await axios.post(
          `http://${process.env.VUE_APP_IP}/history`,
          formData,
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        console.log("Response from server:", response.data);
        this.isSending = false;
      } catch (error) {
        console.error("Error sending data:", error);
        this.isSending = false;
      }
    },
    setActive(index) {
      this.activeIndex = index;
    },
    getDate() {
      const date = new Date();
      const day = `0${date.getDate()}`.slice(-2);
      const month = `0${date.getMonth() + 1}`.slice(-2);
      const year = date.getFullYear();
      this.creationDate = `${day}.${month}.${year}`;
    },
    openFileDialog() {
      this.$refs.dropzoneInput.click();
    },
    removeFile(index) {
      this.fileArr.splice(index, 1);
      this.formDates.fileArr.splice(index, 1);
      if (index === this.activeIndex) {
        this.activeIndex = Math.max(0, index - 1);
      }
    },
    onInput(event) {
      let inputValue = event.target.value.replace(/\D+/g, ""); // remove non-digit characters
      const formattedValue = this.formatPhoneNumber(inputValue);
      event.target.value = formattedValue;
    },
    formatPhoneNumber(phoneNumber) {
      const parts = phoneNumber.match(/(\d{1})(\d{3})(\d{3})(\d{2})(\d{2})/);
      if (parts) {
        return `${parts[1]}-${parts[2]}-${parts[3]}-${parts[4]}-${parts[5]}`;
      } else {
        let formattedPhoneNumber = "";
        for (let i = 0; i < phoneNumber.length; i++) {
          if (i === 1) {
            formattedPhoneNumber += "-";
          } else if (i === 4) {
            formattedPhoneNumber += "-";
          } else if (i === 7) {
            formattedPhoneNumber += "-";
          } else if (i === 9) {
            formattedPhoneNumber += "-";
          }
          formattedPhoneNumber += phoneNumber[i];
        }
        return formattedPhoneNumber;
      }
    },
  },
  watch: {
    firmName(value) {
      if (value) {
        delete this.errors.firmName;
      }
    },
    modelName(value) {
      if (value) {
        delete this.errors.modelName;
      }
    },
    clientName(value) {
      if (value) {
        delete this.errors.clientName;
      }
    },
    clientPhone(value) {
      if (value) {
        delete this.errors.clientPhone;
      }
    },
    clientAddress(value) {
      if (value) {
        delete this.errors.clientAddress;
      }
    },
    executorName(value) {
      if (value) {
        delete this.errors.executorName;
      }
    },
    executorPhone(value) {
      if (value) {
        delete this.errors.executorPhone;
      }
    },
    serviceCenterAddress(value) {
      if (value) {
        delete this.errors.serviceCenterAddress;
      }
    },
    expluatationDate(value) {
      if (value) {
        delete this.errors.expluatationDate;
      }
    },
    serialNumber(value) {
      if (value) {
        delete this.errors.serialNumber;
      }
    },
    fileArr(value) {
      if (value) {
        delete this.errors.files;
      }
    },
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
