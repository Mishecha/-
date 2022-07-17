# Отправка картинок космоса

Этот проект загружает картинки космоса и автоматически отправляет картинки космоса в телеграмм канал.

### Как установить

#### Токен телеграмм бота
Для начала нужно сделать бота в телеграме. Как сделать можно посмотреть [здесь](https://way23.ru/регистрация-бота-в-telegram.html). 
Далее создайте файл .env и вставляете токен бота. 
В env нужно написать так:
```
TELEGRAM_TOKEN=токен бота
```

#### API токен наса
Найти этот токен можно посмотреть [здесь](https://api.nasa.gov/). Также вставите токен API nasa.
В env нужно написать так:
```
NASA_API_KEY=токен nasa
```

#### Создание директорий
Также для проекта необходимо создать директории. Для этого в .env нужно написать их названия:

```
NASA_EPIC_IMAGE_DIRECTORY=image_nasa_epic

NASA_IMAGE_DIRECTORY=image_nasa

SPACEX_IMAGE_DIRECTORY=image_spacex
```

#### Установка времени отправки картинок
Нужно написать переменную с задержкой времени.
Например:
```
DELAY=86400
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```

### Как запустить код

Для того чтобы код работал, надо открыть терминал, написать cd и путь до вашего проекта.

Для скачивания изображений nasa epic нужно написать:

```
python download_photos_days_nasa_epic.py
```

Для скачивания изображений nasa нужно написать:

```
python download_photos_days_nasa.py
```

Для скачивания изображений spacex нужно написать:
```
python download_photos_spacex.py
```

А для того, чтобы картинки отправились, нужно написать:
```
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
