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
        <form @submit.prevent="handleSubmit">
          <div class="text-2xl text-center w-full font-stengazeta px-4 py-4">
            <span class="text-3xl"> Техническое заключение </span><br />от
            <span class="text-red-500"> {{ this.creationDate }} </span>
            № <span class="text-red-500"> {{ this.conclusionNumber }} </span>
          </div>
          <div class="flex w-full">
            <div class="w-8/12 p-2">
              <div
                class="w-full relative flex flex-col border-2 border-gray-300 border-dashed rounded-lg bg-gray-50 py-2 px-4"
              >
                <div
                  class="flex items-center justify-center w-full h-96 relative"
                >
                  <div class="flex justify-center w-full">
                    <img
                      :src="fileArr[activeIndex]?.defect_photo_path"
                      class="w-auto h-96 rounded-lg"
                      alt="active image"
                    />
                    <Rectangle
                      v-for="(defect, index) in fileArr[activeIndex]?.defects ||
                      []"
                      :key="index"
                      :coords="defect.coords"
                      :name="defect.name"
                      @update-defect="updateDefect(activeIndex, index, $event)"
                    />
                  </div>
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
                    <img
                      :src="image.defect_photo_path"
                      class="w-full h-full object-cover"
                    />
                  </div>
                </div>
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
                  pattern="[8]-[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}"
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
                  type="text"
                  class="mt-1 block w-full min-h-28 px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
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
                  inputmode="numeric"
                  pattern="[8]-[0-9]{3}-[0-9]{3}-[0-9]{2}-[0-9]{2}"
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

          <div class="px-2 pt-2">
            <h3 class="text-lg font-medium text-gray-900">
              Техническое заключение
            </h3>
            <textarea
              v-model="this.conclusionText"
              :class="[
                'mt-1 block w-full px-3 py-2 h-32 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                this.errors.conclusionText
                  ? 'border-red-500 focus:border-red-500'
                  : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
              ]"
            >
            </textarea>
            <span
              v-if="this.errors.conclusionText"
              class="text-red-500 text-sm"
            >
              {{ this.errors.conclusionText }}
            </span>
          </div>
          <div class="px-4">
            <span
              class="text-blue-700 text-sm hover:underline hover:text-blue-800 cursor-pointer"
              @click="
                downloadFile(this.id, this.creationDate, this.conclusionNumber)
              "
            >
              Скачать заключение в формате PDF
            </span>
          </div>
          <div class="flex justify-end py-2">
            <button
              type="submit"
              class="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-8 py-2.5 me-2 mb-2 focus:outline-none"
            >
              Сохранить изменения
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
      id: "",
      creationDate: "",
      conclusionNumber: "",
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

      errors: {},
      activeIndex: 0,

      formDates: {
        fileArr: [],
      },
      isSaving: false,
    };
  },
  beforeRouteUpdate(to, from, next) {
    this.isServiceLoading = true;
    this.id = to.params.id;
    this.getHistoryItem().finally(() => {
      this.isServiceLoading = false;
    });
    next();
  },
  methods: {
    onInput(event) {
      let inputValue = event.target.value.replace(/\D+/g, "");
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
    setActive(index) {
      this.activeIndex = index;
    },
    updateDefect(imageIndex, defectIndex, updatedDefect) {
      this.fileArr[imageIndex].defects[defectIndex] = updatedDefect;
    },
    onInput(event) {
      const value = event.target.value.replace(/[^\d-]/g, "");
      event.target.value = value;
    },
    async handleSubmit(event) {
      event.preventDefault();
      this.errors = {};

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
      if (!this.conclusionText) {
        this.errors.conclusionText = "Поле обязательно для заполнения.";
      }

      if (Object.keys(this.errors).length > 0) {
        return;
      }
      const formData = new FormData(event.target);
      formData.append("firmName", this.firmName);
      formData.append("modelName", this.modelName);
      formData.append("expluatationDate", this.expluatationDate);
      formData.append("serialNumber", this.serialNumber);
      formData.append("clientName", this.clientName);
      formData.append("clientPhone", this.clientPhone);
      formData.append("clientAddress", this.clientAddress);
      formData.append("clientDefects", this.clientDefects);
      formData.append("executorName", this.executorName);
      formData.append("executorPhone", this.executorPhone);
      formData.append("serviceCenterAddress", this.serviceCenterAddress);
      formData.append("conclusionText", this.conclusionText);

      if (this.formDates.fileArr && this.formDates.fileArr.length) {
        this.formDates.fileArr.forEach((file, index) => {
          formData.append(`files`, file);
        });
      }
      try {
        this.isSending = true;
        const response = await axios.post(
          `http://${process.env.VUE_APP_IP}:8000/history`,
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
    async getHistoryItem() {
      this.isServiceLoading = true;
      try {
        const response = await axios.get(
          `http://${process.env.VUE_APP_IP}:8000/result/${this.id}`
        );
        this.updateHistoryData(response.data);
      } catch (error) {
        console.error("Error fetching history item:", error);
      } finally {
        this.isServiceLoading = false;
      }
    },
    updateHistoryData(data) {
      this.creationDate = data.created_at;
      this.conclusionNumber = data.appeal_order;
      this.firmName = data.laptop_firm;
      this.modelName = data.laptop_model;
      this.expluatationDate = data.commission_date;
      this.serialNumber = data.laptop_serial_number;
      this.clientName = data.customer_name;
      this.clientPhone = data.customer_phone;
      this.clientAddress = data.customer_address;
      this.executorName = data.executor_name;
      this.executorPhone = data.executor_phone;
      this.serviceCenterAddress = data.executor_address;

      this.fileArr = data.content.map((item) => ({
        defect_photo_path: item.defect_photo_path,
        defects: item.defects.map((defect) => ({
          name: defect.name || defect.class || "Unknown",
          coords: defect.coords,
        })),
      }));
    },
    downloadFile(id, date, name) {
      axios
        .get(`http://${process.env.VUE_APP_IP}/download/${id}`)
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute("download", `Заключение от ${date} № ${name}.pdf`);
          document.body.appendChild(link);
          link.click();
        })
        .catch((error) => {
          console.error("Error downloading file:", error);
        });
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
    $route: {
      async handler(to, from) {
        this.isServiceLoading = true;
        this.id = to.params.id;
        await this.getHistoryItem();
        this.$nextTick(() => {});
        this.isServiceLoading = false;
      },
      immediate: true,
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
