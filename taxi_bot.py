import logging
import sys
from logging import StreamHandler

from telegram import Bot, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (CallbackQueryHandler, Filters, MessageHandler,
                          Updater)
from telegram.ext.commandhandler import CommandHandler

from constans import (BOT_TELEGRAM_TOKEN, ID_CLIENT_TAXI,
                      TELEGRAM_CHAT_ID)
from order_comands import (get_balance_manual, get_employees_all_time,
                           get_employees_last_month, get_employees_year,
                           get_last_order)

bot = Bot(token=BOT_TELEGRAM_TOKEN)
updater = Updater(token=BOT_TELEGRAM_TOKEN)


def button(update, _):
    query = update.callback_query
    variant = query.data
    if variant == 'balance':
        query.answer()
        query.edit_message_text(text=get_balance_manual(ID_CLIENT_TAXI))
    elif variant == 'last_order':
        query.answer()
        query.edit_message_text(text=get_last_order(ID_CLIENT_TAXI))
    # elif variant == 'total_month':
    #     query.answer()
    #     query.edit_message_text(text=get_total_month(ID_CLIENT_TAXI))
    elif variant == 'employees_last_month':
        query.answer()
        query.edit_message_text(text=get_employees_last_month(ID_CLIENT_TAXI))
    elif variant == 'employees_last_year':
        query.answer()
        query.edit_message_text(text=get_employees_year(ID_CLIENT_TAXI))
    elif variant == 'employees_all_time':
        query.answer()
        query.edit_message_text(text=get_employees_all_time(ID_CLIENT_TAXI))


def start(update, context):
    keyboard = [
        [
            InlineKeyboardButton(
                "Баланс Яндекс.Такси", callback_data='balance')],
        [
            InlineKeyboardButton(
                "Последние 5 заказов", callback_data='last_order')],
        # [
        #     InlineKeyboardButton(
        #         "Расходы за месяц", callback_data='total_month')],
        [
            InlineKeyboardButton(
                "Расходы за месяц",
                callback_data='employees_last_month')],
        [
            InlineKeyboardButton(
                "Расходы за год", callback_data='employees_last_year')],
        [
            InlineKeyboardButton(
                "Расходы за все время", callback_data='employees_all_time')],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Чем помочь?', reply_markup=reply_markup)


def help(update, context):
    update.effective_chat
    context.bot.send_message(chat_id=update.message.chat_id, text='/start')


def main():
    print(TELEGRAM_CHAT_ID)
    print(type(TELEGRAM_CHAT_ID))

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s, %(levelname)s, %(message)s, %(name)s'
    )
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = StreamHandler(stream=sys.stdout)
    logger.addHandler(handler)
    while True:
        updater.dispatcher.add_handler(
            CommandHandler('start', start, Filters.user(TELEGRAM_CHAT_ID)))
        updater.dispatcher.add_handler(CallbackQueryHandler(button))
        updater.dispatcher.add_handler(MessageHandler(Filters.text, help))
        updater.start_polling()
        updater.idle()


if __name__ == '__main__':
    main()
