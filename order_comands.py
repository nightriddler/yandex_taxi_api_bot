import datetime
import json
import logging

from constans import TAXI_CLASS, ID_CLIENT_TAXI, YA_TAXI_TOKEN, PAYMENT_LIMIT
from response_comands import get_response_orders, get_response_client


def get_info_order(response: json):
    '''Информация по заказу.'''
    name = response.get('corp_user')['fullname']
    source_start = response.get('source')['fullname'][8:]
    destination = response.get('destination')['fullname'][8:]
    cost_with_vat = response.get('cost_with_vat')
    date = response.get('due_date').replace('T', ' ')

    if (name and source_start and
            destination and cost_with_vat and date) is None:
        logging.exception('Can not get order info')

    cargo_class = TAXI_CLASS[response['class']]
    return (f'{name}\n'
            f'Тариф: {cargo_class}\n'
            f'Когда: {date}\n'
            f'Откуда: {source_start}\n'
            f'Куда: {destination}\n'
            f'Стоимость поездки(с учетом НДС): {cost_with_vat} руб.\n\n')


def get_balance_manual(client: ID_CLIENT_TAXI):
    '''Баланс клиента.'''
    response = get_response_client(client, YA_TAXI_TOKEN)

    balance = response.json().get(
        'services')['drive']['contract_info']['balance']

    if balance is None:
        logging.error('Can not get "balance".')
        return 'Ошибка. Не удается получить значение "balance".'
    status = 'Активный'
    if float(balance) < PAYMENT_LIMIT:
        status = 'Активный, но превышен лимит задолженности'
    if response.json()['is_active'] is False:
        status = 'Заблокирован'

    name = response.json().get('name')
    currency_sign = response.json().get('currency_sign')

    if (name and currency_sign) is None:
        logging.exception(
            'Can not get name or currence_sign in response client')

    return (f'Баланс {name}: {balance} {currency_sign}\n'
            f'Доступный лимит: {PAYMENT_LIMIT} {currency_sign}\n'
            f'Статус: {status}')


# def get_order_last_month(client: ID_CLIENT_TAXI):
#     '''Расходы за месяц. Подробная информация. Может не поместиться в сообщение.'''
#     response = get_response_orders(client, YA_TAXI_TOKEN)
#     answer = ''
#     now = datetime.datetime.now()
#     last_month = now - datetime.timedelta(days=30)
#     for order in response.json()['items']:
#         if order['status']['full'] == 'complete':
#             date_in_order = datetime.datetime.strptime(order['finished_date'], '%Y-%m-%dT%H:%M:%S')
#             if date_in_order >= last_month:
#                 answer += get_info_order(order)
#     return answer


def get_last_order(client: ID_CLIENT_TAXI):
    '''Последние 5 заказов.'''
    response = get_response_orders(client, YA_TAXI_TOKEN, 5)
    answer = ''
    orders = response.json().get('items')
    if orders is None:
        logging.exception('Can not get order from last 5 orders')
    for order in orders:
        if order['status']['full'] == 'complete':
            answer += get_info_order(order)
    return answer


# def get_total_month(client: ID_CLIENT_TAXI):
#     '''Заказы за месяц. Одной строкой.'''
#     response = get_response_orders(client, YA_TAXI_TOKEN, 0)
#     total = int()
#     now = datetime.datetime.now()
#     last_month = now - datetime.timedelta(days=30)
#     for order in response.json()['items']:
#         if order['status']['full'] == 'complete':
#             date_in_order = datetime.datetime.strptime(order['finished_date'], '%Y-%m-%dT%H:%M:%S')
#             if date_in_order > last_month:
#                 total += int(float(order['cost_with_vat']))
#     return f'Расходы c {str(last_month)[:10]} по {str(now)[:10]} (с учетом НДС): {total} руб.'


def calculate_orders_by_period(response, start_time=None):
    '''Расчет суммы заказов по сотруднику за указанный период.'''
    now = datetime.datetime.now()
    starting_point = now - datetime.timedelta(days=start_time)

    employees = {'Заказы из личного кабинета': 0}
    orders = response.json().get('items')
    if orders is None:
        logging.exception('Can not get orders from calculate')
    for order in orders:
        if order['status']['full'] == 'complete':
            date_in_order = datetime.datetime.strptime(
                order['finished_date'], '%Y-%m-%dT%H:%M:%S')
            if date_in_order >= starting_point:
                if order['corp_user'][
                    'fullname'] in employees and len(
                        order['corp_user']['fullname']) != 0:
                    employees[order['corp_user'][
                        'fullname']] += int(float(order['cost_with_vat']))
                elif len(order['corp_user']['fullname']) != 0:
                    employees[order[
                        'corp_user']['fullname']] = int(
                            float(order['cost_with_vat']))
                else:
                    employees[
                        'Заказы из личного кабинета'] += int(float(
                            order['cost_with_vat']))

    result = f'За период с {str(starting_point)[:10]} по {str(now)[:10]}:\n\n'

    sorted_employees = sorted(employees.items(), key=lambda cost: cost[1])
    employees = dict(sorted_employees[::-1])

    for employee in employees:
        result += f'{employee} - {employees[employee]} руб.\n'

    employees['Общая сумма'] = sum(employees.values())
    result += f'\n Общая сумма: {employees["Общая сумма"]} руб.'

    return result


def get_employees_last_month(client: ID_CLIENT_TAXI):
    '''Заказы за месяц с сортировкой по сотрудникам.'''
    response = get_response_orders(client, YA_TAXI_TOKEN, limit=0)
    return calculate_orders_by_period(response, start_time=30)


def get_employees_year(client: ID_CLIENT_TAXI):
    '''Заказы за год с сортировкой по сотрудникам.'''
    response = get_response_orders(client, YA_TAXI_TOKEN, limit=0)
    return calculate_orders_by_period(response, start_time=365)


def get_employees_all_time(client: ID_CLIENT_TAXI):
    '''Заказы за весь период времени с сортировкой по сотрудникам.'''
    response = get_response_orders(client, YA_TAXI_TOKEN, limit=0)
    first_order = get_response_orders(
        client, YA_TAXI_TOKEN, limit=1, sorting_direction=1)
    try:
        data_first_order = datetime.datetime.strptime(
            first_order.json()[
                'items'][0]['finished_date'], '%Y-%m-%dT%H:%M:%S')
    except AttributeError:
        logging.exception('Can not get data from response first order')
    start_time = (datetime.datetime.now()-data_first_order).days
    return calculate_orders_by_period(response, start_time)
