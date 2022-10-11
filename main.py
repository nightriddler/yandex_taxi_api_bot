import datetime
import logging
import sys
from logging import StreamHandler

import pytz
from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    CallbackContext,
    CallbackQueryHandler,
    Filters,
    MessageHandler,
    Updater,
)
from telegram.ext.commandhandler import CommandHandler

from constans import (
    BOT_TELEGRAM_TOKEN,
    ID_CLIENT_TAXI,
    TELEGRAM_CHAT_ID,
    NOTIFICATIONS_TIME,
)
from job import check_balance
from order_comands import get_balance_manual, get_employees_statics, get_last_order

bot = Bot(token=BOT_TELEGRAM_TOKEN)
updater = Updater(token=BOT_TELEGRAM_TOKEN)


def button(update: Updater, _) -> None:
    query = update.callback_query
    variant = query.data
    if variant == "balance":
        query.answer()
        query.edit_message_text(text=get_balance_manual(ID_CLIENT_TAXI))
    elif variant == "last_order":
        query.answer()
        query.edit_message_text(text=get_last_order(ID_CLIENT_TAXI, 5))
    elif variant == "employees_last_month":
        query.answer()
        query.edit_message_text(text=get_employees_statics(ID_CLIENT_TAXI, "month"))
    elif variant == "employees_last_year":
        query.answer()
        query.edit_message_text(text=get_employees_statics(ID_CLIENT_TAXI, "year"))
    elif variant == "employees_all_time":
        query.answer()
        query.edit_message_text(text=get_employees_statics(ID_CLIENT_TAXI, "all"))


def start(update: Updater, _) -> None:
    keyboard = [
        [InlineKeyboardButton("Баланс Яндекс.Такси", callback_data="balance")],
        [InlineKeyboardButton("Последние заказы", callback_data="last_order")],
        [
            InlineKeyboardButton(
                "Расходы за месяц", callback_data="employees_last_month"
            )
        ],
        [InlineKeyboardButton("Расходы за год", callback_data="employees_last_year")],
        [
            InlineKeyboardButton(
                "Расходы за все время", callback_data="employees_all_time"
            )
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text("Чем помочь?", reply_markup=reply_markup)


def help(update: Updater, context: CallbackContext) -> None:
    update.effective_chat
    context.bot.send_message(chat_id=update.message.chat_id, text="/start")


def main() -> None:
    logging.basicConfig(
        level=logging.DEBUG, format="%(asctime)s, %(levelname)s, %(message)s, %(name)s"
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)

    job = updater.job_queue

    job.run_daily(
        callback=check_balance,
        time=datetime.datetime.strptime(NOTIFICATIONS_TIME, "%H:%M")
        .time()
        .replace(tzinfo=pytz.timezone("Europe/Moscow")),
        days=(0, 1, 2, 3, 4),
    )

    while True:

        updater.dispatcher.add_handler(
            CommandHandler("start", start, Filters.user(TELEGRAM_CHAT_ID))
        )
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, help))
        updater.start_polling()
        updater.idle()


if __name__ == "__main__":
    main()
