# В чем *СИЛА*? ![Логотип проекта](logo.png)
  ### *Доброго времени суток!* **Вашему вниманию** представляется сервис по интеллектуальной обработке фотограмметрических данных дефектов ноутбуков, предназначенный для решения проблемы временных затрат на техническую экспертизу. ###

# Требования к эксплуатации
**Для запуска приложения представлены следующие требования:**
1) *PostgreSQL => 14.0*;
2) *Python => 3.11.0*;
3) *Linux* / *Windows*
4) *Библиотеки из poetry.lock и package-lock.json*;
5) *Широкополосное стабильное подключение к ИТКС "Интернет"*;
6) *Docker* 

# Запуск проекта

#### Подключение к БД
  Создайте файл *.env* в корне проекта, напишите в нем данные для подключения к БД PostgreSQL

```python
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=postgres
```

#### Запуск Docker-контейнера

  В корне проекта выполните команду:
  
  `docker compose up -d`, ожидайте готовности БД к подключениям.

#### Модели для детекции

(*https://disk.yandex.ru/d/2oF9bA3lbHIT2A*)

Распаковать в директорию *fastApi/machine_learning/*

#### Виртуальное окружение

Откройте терминал в корне проекта, выполните команды:
```python
pip3 install poetry

poetry install
```

#### FastAPI

В корне проекта, выполнить:

```python
python fastApi/main.py
```

После того как вы запустите свою БД, выполнив команду выше будут подняты инстансы fastApi и PostgreSQL. Далее необходимо запустить клиентскую часть приложения


#### Frontend
В папке `frontend` создайте два файла для подключения клиентской части к серверной:

1) .env
2) .env.production
   
В этих файлах напишите IP-адрес серверной части приложения в формате:

`VUE_APP_IP_CREATE_TZ = *ВАШ IP*:8000`

Откройте терминал в папке `frontend`, выполните команды:

```js

npm install

npm run serve
```

После этого frontend-часть этого проекта будет доступна на *http://localhost:8080/*.

## Принцип работы проекта

Наше решение представляет собой веб-приложение с открытым API, предназначенное для формирования документации службы качества (техническое решение). Кроме того, в приложении реализовано хранение готовых отчетов как с целью непосредственно хранения ретроспективных данных, так и с точки зрения подготовки набор данных для обучения моделей.
Шаблон формирования документов может быть изменен в соотсветвии с требованиями заказчика.

#### Стэк технологий:

FastAPI, VueJS, PostgreSQL, Docker (docker-compose), torch.

### Технические особенности:

В ходе анализа представленного набора данных возникла необходимость сбора дополнительных данных. Кроме того, очевидным стало использование передовых моделей детектирования объектов (*YOLOv11s* & *YOLOv11n*).
Также, в виду несбалансированности классов предложено использование групп дефектов (физические повереждения, отсутсвие деталей, битые пиксели)

### Уникальность:

1. Наличие модуля автоформирования технического решения в формате .docx
2. Хранение истории запросов в целях сбора выборки для обучения на более "тяжелых" моделях
3. Использование нескольких моделей детекции объектов

*[https://disk.yandex.ru/i/kfvFjvoOZgTg2g](https://disk.yandex.ru/i/gRGr_73CxKEwuw)*
