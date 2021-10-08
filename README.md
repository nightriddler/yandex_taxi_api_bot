# Телеграм-бот для сервиса API Яндекс.Такси

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat-square&logo=telegram)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=flat-square&logo=heroku&logoColor=white)

## Описание
Бот для получения статистики клиента в сервисе Яндекс.Такси. 

Запуск бота командой `/start`, вызовет меню с выбором:

- Баланс и статус клиента.

```
Баланс МОЯ_КОМПАНИЯ: -7015.6 ₽
Доступный лимит: -100000 ₽
Статус: Активный
```

- Последние 5 заказов:

```
Петров Василий Иванович
Тариф: Эконом
Когда: 2021-10-08 15:26:00
Откуда: Реутов, Рижский проспект, 51
Куда: Реутов, Вокзальная улица, 23, Станция Псков-Пассажирский
Стоимость поездки(с учетом НДС): 270.00 руб.

Иванов Петр Никонорович
Тариф: Эконом
Когда: 2021-10-08 09:14:00
Откуда: Москва, улица Розы Люксембург, 17/24
Куда: Москва, Коммунальная улица, 73
Стоимость поездки(с учетом НДС): 1840.80 руб.

Иванов Петр Никонорович
Тариф: Эконом
Когда: 2021-10-08 07:10:00
Откуда: Москва, Коммунальная улица, 73
Куда: Москва, Коммунальная улица, 39
Стоимость поездки(с учетом НДС): 751.20 руб.

Ковалев Никита Михайлович
Тариф: Эконом
Когда: 2021-10-08 05:20:00
Откуда: Москва, Вокзальная улица, 23
Куда: Москва, ул. Льва Толстого, 16
Стоимость поездки(с учетом НДС): 2301.20 руб.

Сидоров Роман Артурович
Тариф: Доставка
Когда: 2021-10-04 10:34:00
Откуда: Москва, Кабельный проезд, 8
Куда: Москва, Зеленоград, к120
Стоимость поездки(с учетом НДС): 2226.00 руб.
```

- Расходы за месяц/за год/ все время (выбранный период будет указан в ответе):

```
За период с 2021-09-08 по 2021-10-08:

Ковалев Никита Михайлович - 123034 руб.
Петров Василий Иванович - 3274 руб.
Сидоров Роман Артурович - 1944 руб.
Иванов Петр Никонорович - 1425 руб.
Заказы из личного кабинета - 1099 руб.

 Общая сумма: 130776 руб.
```

## Настройка и деплой бота
1. Клонируем репозиторий 
```
git clone https://github.com/nightriddler/yandex_taxi_api_bot.git
```
2. Устанавливаем виртуальное окружение, активируем его и устанавливаем зависимости.
```
python -m venv venv
source venv/Scripts/activate 
pip install -r requirements.txt
```
3. В папке `yandex_taxi_api_bot` с проектом создаем файл `.env` с переменными окружения:
```
YA_TAXI_TOKEN=<токен-из-личного-кабинета>
ID_CLIENT_TAXI=<ID-клиента-из-личного-кабинета>
BOT_TELEGRAM_TOKEN=<токен-бота>
TELEGRAM_CHAT_ID=00000000,11111111,2222222
PAYMENT_LIMIT=<порог-отключения-из-личного-кабинета>
```
>В `TELEGRAM_CHAT_ID` указать без пробелов через запятую `CHAT ID` пользователей которые могут пользоваться ботом. `CHAT ID` можно получить в боте `@getmyid_bot`.
4. Для старта бота запускаем файл `taxi_bot.py` в корне проекта: 
```
python taxi_bot.py
```
5. Для деплоя на [Heroku.com](https://heroku.com):
- Создайте приложение (кнопка `New` → `Create new app`).
- Привяжите аккаунт на GitHub: зайдите в раздел Deploy, выберите GitHub в разделе Development method и нажмите на кнопку Connect to GitHub.
- После подтверждения действия (вас попросят ввести пароль) укажите название репозитория, в котором находится код
- Нужно передать на сервер переменные окружения. Откройте вкладку Settings и найдите пункт Config Vars. Нажмите Reveal Config Vars и добавьте поочерёдно ключ и значение для каждой переменной из файла `.env`.
>Также для запуска, в корне проекта лежит `Procfile` в котором указан файл который должен быть запущен на сервере.
- Чтобы запустить приложение, необходимо перейти во вкладку Resources и активировать переключатель напротив строки `worker python taxi_bot.py`

## Документация
[Документация API Яндекс.Такси](https://yandex.ru/dev/taxi/doc/business-api/concepts/request-central.html)

## Связаться с автором
>[LinkedIn](http://linkedin.com/in/aizi)

>[Telegram](https://t.me/nightriddler)

>[Портфолио](https://github.com/nightriddler)