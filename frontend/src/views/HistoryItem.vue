<template>
  <div class="h-full w-full p-2">
    <div
      class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full flex flex-col flex-grow overflow-y-auto"
    >
      <div class="">
        <Success :state="this.isSuccess" />
      </div>
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
                class="flex flex-col border-2 border-gray-300 border-dashed rounded-lg bg-gray-50 p-4"
              >
                <div class="w-full flex gap-4">
                  <div class="relative">
                    <img
                      :src="fileArr[activeIndex]?.defect_photo_path"
                      alt="active image"
                      @load="handleImageLoad"
                      ref="imageElement"
                      class="w-2/3 rounded-lg"
                    />
                    <Rectangle
                      v-for="(defect, index) in fileArr[activeIndex]?.defects ||
                      []"
                      :key="index"
                      :coords="scaleCoords(defect.coords)"
                      :name="defect.name"
                      @update-defect="updateDefect(activeIndex, index, $event)"
                    />
                  </div>

                  <div class="flex flex-col w-1/3 space-y-4 mx-4">
                    <h2 class="text-lg text-center font-semibold">
                      Редактировать дефекты
                    </h2>
                    <div
                      v-for="(defect, index) in fileArr[activeIndex]?.defects ||
                      []"
                      :key="index"
                      class="flex items-center space-x-2"
                    >
                      <div class="w-full flex flex-col">
                        <span class="font-medium text-sm"
                          >Дефект {{ index + 1 }}:</span
                        >
                        <input
                          v-model="fileArr[activeIndex].defects[index].name"
                          class="border border-gray-300 rounded px-2 py-1 mt-2"
                          @input="
                            updateDefectName(
                              activeIndex,
                              index,
                              $event.target.value
                            )
                          "
                        />
                      </div>
                    </div>
                  </div>
                </div>
                <div
                  class="flex items-center space-x-2 mt-4 overflow-x-auto max-w-[40vw] mx-auto custom-scroll"
                >
                  <div
                    v-for="(image, index) in fileArr"
                    :key="index"
                    class="w-24 h-24 border-2 rounded-md overflow-hidden cursor-pointer flex-shrink-0 relative"
                    :class="{ 'border-yellow-500': index == activeIndex }"
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
                  type="text"
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
          <div class="pt-4">
            <button
              @click="downloadFile()"
              type="button"
              class="px-4 py-2 bg-orange-600 rounded-md text-white outline-none shadow-lg duration-100 hover:bg-orange-700 mx-2 flex"
            >
              <svg
                class="h-6 w-6"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"
                />
              </svg>

              <span class="ml-2">Скачать заключение в формате DOCX</span>
            </button>
          </div>
          <div class="flex justify-end py-2">
            <button
              v-if="this.isSaving"
              disabled
              type="button"
              class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-5 py-2.5 text-center me-2 dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800 inline-flex items-center"
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
              Сохранение...
            </button>
            <button
              v-else
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
import Rectangle from "@/components/Rectangle.vue";
import Success from "@/components/Success.vue";
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
      conclusionText: "Необходимо дополнительное обслуживание.",
      fileArr: [],

      isSuccess: false,
      isServiceLoading: false,
      isSaving: false,

      errors: {},
      activeIndex: 0,

      originalWidth: 0,
      originalHeight: 0,
      displayWidth: 0,
      displayHeight: 0,
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

  components: { Rectangle, Success },
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
    updateDefect(index, defectIndex, updatedDefect) {
      this.fileArr[index].defects.splice(defectIndex, 1, updatedDefect);
    },
    updateDefectName(imageIndex, defectIndex, newName) {
      this.fileArr[imageIndex].defects[defectIndex].name = newName;
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

      try {
        this.isSending = true;
        this.isSaving = true;
        const file_arr = this.fileArr;
        const response = await axios.post(
          `http://${process.env.VUE_APP_IP}:8000/update_appeal/${this.id}`,
          { formData, file_arr },
          {
            headers: { "Content-Type": "multipart/form-data" },
          }
        );
        console.log("Response from server:", response.data);
        this.isSending = false;
        this.isSaving = false;
        this.isSuccess = true;
        setTimeout(() => {
          this.isSuccess = false;
        }, 2000);
      } catch (error) {
        console.error("Error sending data:", error);
        this.isSending = false;
        this.isSaving = false;
        this.isSuccess = true;
        setTimeout(() => {
          this.isSuccess = false;
        }, 2000);
      }
    },
    async getHistoryItem() {
      this.isServiceLoading = true;
      try {
        const response = await axios.get(
          `http://${process.env.VUE_APP_IP}:8000/result/${this.id}`
        );
        console.log("Response from server:", response.data);
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
        defect_photo_path: `http://${process.env.VUE_APP_IP}:8000${item.defect_photo_path}`,
        defects: item.defects.map((defect) => ({
          name: defect.name || defect.class || "Unknown",
          coords: defect.coords,
        })),
      }));
    },
    downloadFile() {
      axios
        .get(`http://${process.env.VUE_APP_IP}:8000/doc_by_uuid/${this.id}`, {
          responseType: "blob",
        })
        .then((response) => {
          const url = window.URL.createObjectURL(new Blob([response.data]));
          const link = document.createElement("a");
          link.href = url;
          link.setAttribute(
            "download",
            `Заключение от ${this.creationDate} № ${this.conclusionNumber}.docx`
          );
          document.body.appendChild(link);
          link.click();
          link.remove();
        })
        .catch((error) => {
          console.error("Error downloading file:", error);
        });
    },
    handleImageLoad(event) {
      const { naturalWidth, naturalHeight } = event.target;
      this.originalWidth = naturalWidth;
      this.originalHeight = naturalHeight;

      this.$nextTick(() => {
        const { clientWidth, clientHeight } = this.$refs.imageElement;
        this.displayWidth = clientWidth;
        this.displayHeight = clientHeight;
      });
    },
    scaleCoords(coords) {
      const scaleX = this.displayWidth / this.originalWidth;
      const scaleY = this.displayHeight / this.originalHeight;
      return [
        coords[0] * scaleX,
        coords[1] * scaleY,
        coords[2] * scaleX,
        coords[3] * scaleY,
      ];
    },
    updateDefect(activeIndex, index, { coords, name }) {
      const scaleX = this.originalWidth / this.displayWidth;
      const scaleY = this.originalHeight / this.displayHeight;
      const newCoords = [
        coords[0] * scaleX,
        coords[1] * scaleY,
        coords[2] * scaleX,
        coords[3] * scaleY,
      ];

      this.fileArr[activeIndex].defects[index] = {
        ...this.fileArr[activeIndex].defects[index],
        coords: newCoords,
        name,
      };
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
