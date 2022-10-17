from telegram.ext import CallbackContext

from constans import (
    ID_CLIENT_TAXI,
    YA_TAXI_TOKEN,
    NOTIFICATIONS_CHAT_ID,
    NOTIFICATIONS_LIMIT,
)
from order_comands import get_balance_and_limit_and_curr_sign


def check_balance(context: CallbackContext) -> None:
    balance, payment_limit, currency_sign = get_balance_and_limit_and_curr_sign(
        ID_CLIENT_TAXI, YA_TAXI_TOKEN
    )
    remainder = round(abs(float(payment_limit)) - abs(float(balance)), 2)
    if remainder <= NOTIFICATIONS_LIMIT:
        for user_id in NOTIFICATIONS_CHAT_ID:
            context.bot.send_message(
                chat_id=user_id,
                text=f"Остаток на счете {remainder} {currency_sign}.\nПополните баланс.",
            )
