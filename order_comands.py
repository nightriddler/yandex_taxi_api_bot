import datetime
import json
import logging
from typing import Tuple

from requests import Response

from constans import SYMBOLS, TAXI_CLASS, YA_TAXI_TOKEN
from response_comands import (
    get_response_client,
    get_response_client_balance,
    get_response_orders,
)


def get_clear_data(data: str) -> str or None:
    """Получение короткой читаемой информации."""
    try:
        current_list = data.split(", ")
    except AttributeError:
        return None
    if len(current_list) <= 3:
        interval = 0
    else:
        interval = -4 if len(current_list[-3]) <= 2 else -3
    return ", ".join(current_list[interval:])


def get_balance_and_limit_and_curr_sign(
    client: str, token: str
) -> Tuple[int, int, int]:
    """Получить кортеж из баланса, лимита и символа валюты."""
    response_balance = get_response_client_balance(client, token)
    response_client = get_response_client(client, token)

    balance = response_balance.json().get("contracts")[0]["balances"]["balance"]
    payment_limit = response_balance.json().get("contracts")[0]["settings"][
        "prepaid_deactivate_threshold"
    ]
    currency_sign = response_client.json().get("currency_sign")
    return (balance, payment_limit, currency_sign)


def get_info_order(client: str, response: json) -> str:
    """Получить строку информаии по заказу."""
    name = response.get("corp_user")["fullname"]
    source_start = response.get("source")["fullname"]
    destination = response.get("destination")["fullname"]

    source_start = get_clear_data(source_start)
    destination = get_clear_data(destination)

    cost_with_vat = response.get("cost_with_vat")

    date_dt = datetime.datetime.strptime(
        response.get("finished_date"), "%Y-%m-%dT%H:%M:%S"
    )
    date = date_dt.strftime("%d.%m.%Y %H:%M:%S")

    get_distance = get_response_orders(client, YA_TAXI_TOKEN, order=response.get("_id"))
    distance = get_distance.json().get("distance")

    if (name and source_start and destination and cost_with_vat and date) is None:
        logging.exception("Can not get order info")

    cargo_class = TAXI_CLASS[response["class"]]
    return (
        f'{SYMBOLS["person"]} {name}\n'
        f'{SYMBOLS["taxi"]} {cargo_class}\n'
        f'{SYMBOLS["time"]} {date}\n'
        f'{SYMBOLS["start"]} {source_start}\n'
        f'{SYMBOLS["finish"]} {destination}\n'
        f'{SYMBOLS["distance"]} {round(distance/1000,1)} км.\n'
        f'{SYMBOLS["credit_card"]} {cost_with_vat} руб.\n\n'
    )


def get_balance_manual(client: str) -> str:
    """Получить строку баланса клиента."""
    balance, payment_limit, currency_sign = get_balance_and_limit_and_curr_sign(
        client, YA_TAXI_TOKEN
    )
    response_client = get_response_client(client, YA_TAXI_TOKEN)

    if balance is None:
        logging.error('Can not get "balance".')
        return 'Ошибка. Не удается получить значение "balance".'

    status = "Активный"
    if float(balance) < float(payment_limit):
        status = "Активный, но превышен лимит задолженности"
    if response_client.json().get("is_active") is False:
        status = "Заблокирован"

    name = response_client.json().get("name")

    if (name and currency_sign) is None:
        logging.exception("Can not get name or currence_sign in response client")

    return (
        f'{SYMBOLS["case"]} {name}: {balance} {currency_sign}\n'
        f"Лимит: {payment_limit} {currency_sign}\n"
        f"Статус: {status}"
    )


def get_last_order(client: str, amount_orders: int) -> str:
    """Получить строку из последних "amount_orders" заказов."""
    response = get_response_orders(client, YA_TAXI_TOKEN)
    answer = ""
    orders = response.json().get("items")
    if orders is None:
        logging.exception("Can not get order from last 5 orders")
    for order in orders:
        if order["status"]["full"] == "complete":
            answer += get_info_order(client, order)
            amount_orders -= 1
        if amount_orders == 0:
            break
    return answer


def calculate_orders_by_period(response: Response, start_time: int = None) -> str:
    """Получение строки результата расчета суммы заказов по сотруднику за указанный период."""
    now = datetime.datetime.now()
    starting_point = now - datetime.timedelta(days=start_time)

    employees = {"Заказы из личного кабинета": 0}
    orders = response.json().get("items")
    if orders is None:
        logging.exception("Can not get orders from calculate")
    for order in orders:
        if order["status"]["full"] == "complete":
            date_in_order = datetime.datetime.strptime(
                order["finished_date"], "%Y-%m-%dT%H:%M:%S"
            )
            if date_in_order >= starting_point:
                if (
                    order["corp_user"]["fullname"] in employees
                    and len(order["corp_user"]["fullname"]) != 0
                ):
                    employees[order["corp_user"]["fullname"]] += int(
                        float(order["cost_with_vat"])
                    )
                elif len(order["corp_user"]["fullname"]) != 0:
                    employees[order["corp_user"]["fullname"]] = int(
                        float(order["cost_with_vat"])
                    )
                else:
                    employees["Заказы из личного кабинета"] += int(
                        float(order["cost_with_vat"])
                    )

    result = (
        f'Расходы с {starting_point.strftime("%d.%m.%Y")} '
        f'по {now.strftime("%d.%m.%Y")}:\n\n'
    )

    sorted_employees = sorted(employees.items(), key=lambda cost: cost[1])
    employees = dict(sorted_employees[::-1])

    for employee in employees:
        result += f"{employee} - {employees[employee]} руб.\n"

    employees["Общая сумма"] = sum(employees.values())
    result += f'\n {SYMBOLS["credit_card"]} {employees["Общая сумма"]} руб.'

    return result


def get_employees_statics(client: str, period: str) -> str:
    """Получить строку статистики заказов за указанный период всех сотрудников."""
    response = get_response_orders(client, YA_TAXI_TOKEN, limit=0)
    if period == "month":
        return calculate_orders_by_period(response, start_time=30)
    elif period == "year":
        return calculate_orders_by_period(response, start_time=365)
    elif period == "all":
        first_order = get_response_orders(
            client, YA_TAXI_TOKEN, limit=1, sorting_direction=1
        )
        try:
            data_first_order = datetime.datetime.strptime(
                first_order.json()["items"][0]["finished_date"], "%Y-%m-%dT%H:%M:%S"
            )
        except AttributeError:
            logging.exception("Can not get data from response first order")
        start_time = (datetime.datetime.now() - data_first_order).days
        return calculate_orders_by_period(response, start_time)
