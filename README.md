# Отправка картинок космоса

Этот проект создан для того, что бы вы могли сокращать ссылки и узнавать сколько людей 
перешло по ссылке. 

### Как установить

#### Токен бота
Для начала нужно сделать бота в телеграме. Как сделать можно посмотреть [здесь](https://way23.ru/регистрация-бота-в-telegram.html). 
Далее создайте файл .env и вставить токен бота. 
В env нужно написать так:
```
TELEGRAM_TOKEN=токен бота
```

#### апи токен наса
Найти этот токен можно посмотреть [здесь](https://api.nasa.gov/). Также вставить токен апи наса.
В env нужно написать так:
```
NASA_API_KEY=токен наса
```

#### Установка времени отправки картинок
Надо написать переменную с задержкой времени.
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

для того чтобы код работал, надо открыть терминал, написать cd и путь до вашего проекта, после написать

```
python main.py
```

### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).