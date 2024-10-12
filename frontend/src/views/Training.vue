<template>
    <div class="h-full w-full p-2">
        <div
            class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full flex flex-col flex-grow overflow-y-auto">
            <div v-if="this.isServiceLoading" class="h-full w-full flex flex-col justify-center items-center">
                <span class="loader"></span>
                <p class="text-black pt-2 font-stengazeta text-sm">
                    Идет загрузка формы...
                </p>
            </div>
            <div v-else class="flex flex-col">
                <form @submit.prevent="handleSubmit">
                    <div class="flex w-full">
                        <div class="w-8/12 p-2">
                            <div
                                class="w-full relative flex flex-col border-2 border-gray-300 border-dashed rounded-lg bg-gray-50 py-2 my-8 px-4">
                                <div class="flex items-center justify-center w-full h-96">
                                    <div class="flex justify-center w-full">
                                        <div class="flex justify-center w-full">
                                            <img :src="fileArr[this.activeIndex]" class="w-auto h-96 rounded-lg"
                                                alt="active image" />
                                        </div>
                                    </div>
                                </div>

                                <div
                                    class="flex items-center space-x-2 mt-4 overflow-x-auto max-w-[40vw] mx-auto custom-scroll">
                                    <div v-for="(image, index) in fileArr" :key="index"
                                        class="w-24 h-24 border-2 rounded-md overflow-hidden cursor-pointer flex-shrink-0 relative"
                                        :class="{
                                            'border-yellow-500': index == this.activeIndex,
                                        }" @click="setActive(index)">
                                        <img :src="image" class="w-full h-full object-cover" />
                                    </div>
                                </div>
                            </div>
                        </div>
                        <div class="w-4/12 h-full p-2 flex flex-col gap-2">
                            <p class="font-bold text-xl text-center">Гиперпараметры модели</p>
                            <label class="block">
                                <span class="block text-sm font-medium text-gray-700">Тип модели</span>
                                <select v-model="selectedModel" placeholder="Выберите модель" :class="[
                                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                                    this.errors.firmName
                                        ? 'border-red-500 focus:border-red-500'
                                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                                ]">
                                    <option v-for="(type, index) in modelType" :key="index">{{ type.legend }}</option>
                                </select>
                                <span v-if="this.errors.selectedModel" class="text-red-500 text-sm">
                                    {{ this.errors.selectedModel }}
                                </span>
                            </label>
                            <label class="block">
                                <span class="block text-sm font-medium text-gray-700">Количество эпох</span>
                                <input  v-model="this.epochs" type="number" min="1" pattern="\d+" placeholder="Введите количество эпох" step="1" :class="[
                                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                                    this.errors.epochs
                                        ? 'border-red-500 focus:border-red-500'
                                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                                ]" />
                                <span v-if="this.errors.epochs" class="text-red-500 text-sm">
                                    {{ this.errors.epochs }}
                                </span>
                            </label>
                            <label class="block">
                                <span class="block text-sm font-medium text-gray-700">Размер входного окна (batch size)</span>
                                <input  v-model="this.batchSize" type="number" min="1" pattern="\d+" placeholder="Введите количество эпох" step="1" :class="[
                                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                                    this.errors.batchSize
                                        ? 'border-red-500 focus:border-red-500'
                                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                                ]" />
                                <span v-if="this.errors.batchSize" class="text-red-500 text-sm">
                                    {{ this.errors.batchSize }}
                                </span>
                            </label>
                            <div>
                                <label class="block">
                                    <span class="block text-sm font-medium text-gray-700">Период сохранения модели, эпохи</span>
                                    <input  v-model="this.savePeriod" type="number" min="1" pattern="\d+" placeholder="Введите количество эпох" step="1" :class="[
                                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                                    this.errors.savePeriod
                                        ? 'border-red-500 focus:border-red-500'
                                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                                ]" />
                                </label>
                                <span v-if="this.errors.savePeriod" class="text-red-500 text-sm">
                                    {{ this.errors.savePeriod }}
                                </span>
                            </div>
                            <div>
                                <label class="block">
                                    <span class="block text-sm font-medium text-gray-700">Скорость обучения</span>
                                    <input  v-model="this.learningRate" type="number" min="0.001" max="1"  placeholder="Введите количество эпох" step="0.1" :class="[
                                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                                    this.errors.learningRate
                                        ? 'border-red-500 focus:border-red-500'
                                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                                ]" />
                                </label>
                                <span v-if="this.errors.learningRate" class="text-red-500 text-sm">
                                    {{ this.errors.learningRate }}
                                </span>
                            </div>
                            <div>
                                <label class="block">
                                    <span class="block text-sm font-medium text-gray-700">Оптимизаторы</span>
                                    <select v-model="selectedOptimizer" placeholder="Выберите модель" :class="[
                                    'mt-1 block w-full px-3 py-2 bg-white border rounded-md shadow-sm focus:outline-none sm:text-sm',
                                    this.errors.firmName
                                        ? 'border-red-500 focus:border-red-500'
                                        : 'border-gray-300 focus:ring-indigo-500 focus:border-indigo-500',
                                ]">
                                    <option v-for="(optimizer, index) in optimizers" :key="index">{{ optimizer }}</option>
                                </select>
                                <span v-if="this.errors.selectedModel" class="text-red-500 text-sm">
                                    {{ this.errors.selectedModel }}
                                </span>
                                </label>
                            </div>
                        </div>
                    </div>
                    <div class="flex justify-center ">
                        <button type="submit"
                            class="text-white bg-blue-600 hover:bg-blue-700 font-medium rounded-lg text-sm px-11 py-4 me-2 mb-2 focus:outline-none">
                            НАЧАТЬ ОБУЧЕНИЕ
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
            id: null,
            epochs: 100,
            batchSize: 16,
            savePeriod: 15,
            fileArr: [],
            learningRate: 0.5,
            selectedModel: "Точная",
            modelType: [
                {
                    legend: "Быстрая",
                    name: "yolov11.pt"
                },
                {
                    legend: "Оптимальная",
                    name: "yolov11.pt"
                },
                {
                    legend: "Точная",
                    name: "yolov11.pt"
                },
            ],
            optimizers: [
                "SGD", "Adam", "AdamW", "NAdam", "RAdam", "RMSProp", "auto"
            ],
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
    // mounted() {
    //   this.isServiceLoading = true;
    //   this.id = this.$route.params.id;
    //   this.getHistoryItem();
    // },
    methods: {
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
        setActive(index) {
            this.activeIndex = index;
        },
        async handleSubmit(event) {
            event.preventDefault();
            this.errors = {};

            if (!this.firmName) {
                this.errors.selectedModel = "Поле обязательно для заполнения.";
            }
            if (!this.modelName) {
                this.errors.epochs = "Поле обязательно для заполнения.";
            }
            if (!this.batchSize) {
                this.errors.batchSize = "Поле обязательно для заполнения.";
            }
            if (!this.savePeriod) {
                this.errors.savePeriod = "Поле обязательно для заполнения.";
            }
            if (!this.clientName) {
                this.errors.learningRate = "Поле обязательно для заполнения.";
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
            formData.append("conclusionText", this.conclusionText);

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
        getHistoryItem() {
            axios
                .get(`http://${process.env.VUE_APP_IP}/statement/${this.id}`)
                .then((response) => {
                    this.updateHistoryData(response.data);
                })
                .catch((error) => {
                    console.error("Error fetching history item:", error);
                })
                .finally(() => {
                    this.isServiceLoading = false;
                });
        },
        updateHistoryData(data) {
            this.firmName = data.firmName || "Default Firm Name";
            this.modelName = data.modelName || "Default Model Name";
            this.creationDate = data.creationDate || "Default Creation Date";
            this.expluatationDate =
                data.expluatationDate || "Default Exploitation Date";
            this.serialNumber = data.serialNumber || "Default Serial Number";
            this.clientName = data.clientName || "Default Client Name";
            this.clientPhone = data.clientPhone || "Default Client Phone";
            this.clientAddress = data.clientAddress || "Default Client Address";
            this.clientDefects = data.clientDefects || "Default Client Defects";
            this.executorName = data.executorName || "Default Executor Name";
            this.executorPhone = data.executorPhone || "Default Executor Phone";
            this.serviceCenterAddress =
                data.serviceCenterAddress || "Default Service Center Address";
            this.conclusionText = data.conclusionText || "Default Conclusion Text";
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