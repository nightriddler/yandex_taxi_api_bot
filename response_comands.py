import logging

import requests
from requests.exceptions import RequestException


def get_response_orders(
    client, token, limit=100, sorting_direction=-1, order=None
):
    '''Получение заказа/заказов по указанному лимиту.
    limit - количество заказов (0 - за все время).
    sorting_direction - направление сортировки (-1 и 1).
    order - получение заказа по id (по-умолчанию None.'''
    if order:
        try:
            response = requests.get(
                f'https://business.taxi.yandex.ru/api/1.0/client/'
                f'{client}/order/{order}',
                headers={'Authorization': token})
        except RequestException:
            logging.exception('Can not get response orders.')
            return {}
        return response
    try:
        response = requests.get(
            f'https://business.taxi.yandex.ru/api/1.0/client/'
            f'{client}/order?{limit=}&{sorting_direction=}',
            headers={'Authorization': token})
    except RequestException:
        logging.exception('Can not get response orders.')
        return {}
    return response


def get_response_client(client, token):
    '''Информация о клиенте.'''
    try:
        response = requests.get(
            f'https://business.taxi.yandex.ru/api/1.0/client/{client}/',
            headers={'Authorization': token})
    except RequestException:
        logging.exception('Can not get response client.')
        return {}
    return response
