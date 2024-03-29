# Телеграм-бот для сервиса API Яндекс.Такси

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
![Telegram](https://img.shields.io/badge/Telegram-2CA5E0?style=flat-square&logo=telegram)
![Heroku](https://img.shields.io/badge/heroku-%23430098.svg?style=flat-square&logo=heroku&logoColor=white)

### Последние обновления
- Добавлена рассылка при сумме остатка 1000 рублей.

## Описание
Бот для получения статистики клиента в сервисе Яндекс.Такси. 

Запуск бота командой `/start`, вызовет меню с выбором:

- Баланс и статус клиента.

```
💼 МОЯ_КОМПАНИЯ: -7015.6 ₽
Доступный лимит: -100000 ₽
Статус: Активный
```

- Последние 5 заказов:

```
👤 Ковалев Никита Михайлович
🚕 Élite
🕝 08.10.2021 15:26:00
🛫 Москва, Вокзальная улица, 23
🛬 Москва, ул. Льва Толстого, 16
🧭 77.7 км.
💳 2301.20 руб.

👤 Иванов Петр Никонорович
🚕 Эконом
🕝 08.10.2021 09:14:00
🛫 Москва, улица Розы Люксембург, 17/24
🛬 Москва, Коммунальная улица, 73
🧭 3.3 км.
💳 1840.80 руб.

👤 Иванов Петр Никонорович
🚕 Эконом
🕝 08.10.2021 07:10:00
🛫 Москва, Коммунальная улица, 73
🛬 Москва, Коммунальная улица, 39
🧭 1.2 км.
💳 751.20 руб.

👤 Петров Василий Иванович
🚕 Эконом
🕝 08.10.2021 05:20:00
🛫 Реутов, Рижский проспект, 51
🛬 Реутов, Вокзальная улица, 23, Станция Псков-Пассажирский
🧭 7.9 км.
💳 270.00 руб.

👤 Сидоров Роман Артурович
🚕 Доставка
🕝 04.10.2021 10:34:00
🛫 Москва, Кабельный проезд, 8
🛬 Москва, Зеленоград, к120
🧭 120.1 км.
💳 2226.00 руб.
```

- Расходы за месяц/за год/все время (выбранный период будет указан в ответе):

```
Расходы с 08.09.2021 по 08.10.2021:

Ковалев Никита Михайлович - 123034 руб.
Петров Василий Иванович - 3274 руб.
Сидоров Роман Артурович - 1944 руб.
Иванов Петр Никонорович - 1425 руб.
Заказы из личного кабинета - 1099 руб.

💳 130776 руб.
```

- Ежедневная рассылка выбранным пользователям при сумме остатка ниже 1000 рублей.

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
3. В папке с проектом создаем файл `.env` с переменными окружения:
```
YA_TAXI_TOKEN=<токен-из-личного-кабинета>
ID_CLIENT_TAXI=<ID-клиента-из-личного-кабинета>
BOT_TELEGRAM_TOKEN=<токен-бота>
TELEGRAM_CHAT_ID=00000000,11111111,2222222
NOTIFICATIONS_CHAT_ID=00000000,11111111
NOTIFICATIONS_TIME=12:00
NOTIFICATIONS_LIMIT=1000
```
>В `TELEGRAM_CHAT_ID` указать без пробелов через запятую `CHAT ID` пользователей которые могут пользоваться ботом. `CHAT ID` можно получить в боте `@getmyid_bot`.

Настройка рассылки:
- `NOTIFICATIONS_CHAT_ID` - `CHAT ID` пользователей участвующие в рассылке
- `NOTIFICATIONS_TIME` - время рассылки в формате `24:00`
- `NOTIFICATIONS_LIMIT` - размер остатка для уведомления

4. Для старта бота запускаем файл `main.py` в корне проекта: 
```
python main.py
```
5. Для деплоя на [Heroku.com](https://heroku.com):
- Создайте приложение (кнопка `New` → `Create new app`).
- Привяжите аккаунт на GitHub: зайдите в раздел Deploy, выберите GitHub в разделе Development method и нажмите на кнопку Connect to GitHub.
- После подтверждения действия (вас попросят ввести пароль) укажите название репозитория, в котором находится код
- Нужно передать на сервер переменные окружения. Откройте вкладку Settings и найдите пункт Config Vars. Нажмите Reveal Config Vars и добавьте поочерёдно ключ и значение для каждой переменной из файла `.env`.
>Также для запуска, в корне проекта лежит `Procfile` в котором указан файл который должен быть запущен на сервере.
- Чтобы запустить приложение, необходимо перейти во вкладку Resources и активировать переключатель напротив строки `worker python main.py`


## Документация
[Документация API Яндекс.Такси](https://yandex.ru/dev/taxi/doc/business-api/concepts/request-central.html)

## Связаться с автором
>[LinkedIn](http://linkedin.com/in/aizi)

>[Telegram](https://t.me/nightriddler)

>[Портфолио](https://github.com/nightriddler)
