import os

from dotenv import load_dotenv

load_dotenv()

YA_TAXI_TOKEN = os.getenv('YA_TAXI_TOKEN')
ID_CLIENT_TAXI = os.getenv('ID_CLIENT_TAXI')
BOT_TELEGRAM_TOKEN = os.getenv('BOT_TELEGRAM_TOKEN')
TELEGRAM_CHAT_ID = [int(id) for id in os.getenv('TELEGRAM_CHAT_ID').split(',')]

PAYMENT_LIMIT = int(os.getenv('PAYMENT_LIMIT'))
TAXI_CLASS = {
    "vip": "Business",
    "premium_van": "Cruise",
    "ultimate": "Premier",
    "maybach": "Élite",
    "cargo": "Грузовой",
    "child_tariff": "Детский",
    "express": "Доставка",
    "business": "Комфорт",
    "comfortplus": "Комфорт+",
    "courier": "Курьер",
    "minivan": "Минивэн",
    "econom": "Эконом",
}
