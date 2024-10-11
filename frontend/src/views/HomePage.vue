<template>
  <div class="h-full w-full p-2">
    <div
      class="outline-1 outline shadow-[0_0px_5px_2px_rgba(0,0,0,0.1)] rounded-[5px] h-full flex flex-col"
    >
      <p class="text-2xl text-center w-full font-stengazeta px-4 py-4">
        <span class="text-3xl"> Техническое заключение </span><br />от
        <span class="text-red-500"> 23.12.2022 </span>
        №<span class="text-red-500"> 813872387 </span>
      </p>
      <div class="flex w-full">
        <div class="w-8/12 p-2">
          <div class="flex items-center justify-center w-full">
            <label
              for="dropzone-file"
              class="flex flex-col items-center justify-center w-full h-96 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 hover:bg-gray-100"
            >
              <div class="flex flex-col items-center justify-center pt-5 pb-6">
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
                <p class="mb-2 text-gray-500 text-md">
                  <span class="font-semibold">Нажмите чтобы загрузить</span> или
                  перенесите файлы
                </p>
                <p class="text-xs text-gray-500 text-md">PNG, JPG</p>
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
        <div class="w-4/12 p-2 flex flex-col gap-2">
          <label class="block">
            <span class="block text-sm font-medium text-gray-700">Фирма</span>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </label>
          <label class="block">
            <span class="block text-sm font-medium text-gray-700">Модель</span>
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </label>
          <label class="block">
            <span class="block text-sm font-medium text-gray-700"
              >Серийный номер</span
            >
            <input
              type="text"
              class="mt-1 block w-full px-3 py-2 bg-white border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 sm:text-sm"
            />
          </label>
          <p class="text-center text-sm">или загрузите файл</p>
          <div>
            <input
              class="block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50"
              aria-describedby="file_input_help"
              id="file_input"
              type="file"
            />
          </div>
        </div>
      </div>
      <div>
        <div></div>
        <div></div>
      </div>
      <div class="p-2">
        <h3 class="text-lg font-medium text-gray-900">
          Техническое заключение
        </h3>
        <p class="mt-2 text-sm text-gray-600">
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do
          eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad
          minim veniam, quis nostrud exercitation ullamco laboris nisi ut
          aliquip ex ea commodo consequat. Duis aute irure dolor in
          reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla
          pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
          culpa qui officia deserunt mollit anim id est laborum.
        </p>
      </div>
    </div>
  </div>
</template>

<script setup></script>
