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
SYMBOLS = {
    'start': b'\xF0\x9F\x9B\xAB'.decode('utf-8'),
    'finish': b'\xF0\x9F\x9B\xAC'.decode('utf-8'),
    'person': b'\xF0\x9F\x91\xA4'.decode('utf-8'),
    'taxi': b'\xF0\x9F\x9A\x95'.decode('utf-8'),
    'time': b'\xF0\x9F\x95\x9D'.decode('utf-8'),
    'distance': b'\xF0\x9F\xA7\xAD'.decode('utf-8'),
    'credit_card': b'\xF0\x9F\x92\xB3'.decode('utf-8'),
    'case': b'\xF0\x9F\x92\xBC'.decode('utf-8'),
}
