import requests
import time
from config import config
from requests import exceptions


"""
class MyException(Exception):
    pass

class JSONException(MyException):
    pass
"""


def get(query, params={}, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param query: тело GET запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    for n in range(max_retries):
        try:
            response = requests.get(query, params=params, timeout=timeout)
            content_type = response.headers.get('Content-Type')
            if not content_type == "application/json; charset=utf-8":
                raise
            return response
        except requests.exceptions.RequestException:
            if n == max_retries - 1:
                raise
            backoff_value = backoff_factor * (2 ** n)
            time.sleep(backoff_value)


def get_friends(user_id, fields=''):
    """ Returns a list of user IDs or detailed\
    information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'access_token': config.get("ACCESS_TOKEN"),
        'user_id': user_id,
        'fields': fields,
        'v': config.get('v')
    }
    url = "{}/friends.get".format(config.get("DOMAIN"))
    response = get(url, params=query_params)
    return response.json()


def get_messages_history(user_id, offset=0, count=200):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    max_count = 200
    query_params = {
        'domain': config.get("DOMAIN"),
        'access_token': config.get("ACCESS_TOKEN"),
        'user_id': user_id,
        'offset': offset,
        'count': min(count, max_count),
        'v': config.get('v')
    }
    messages = []

    while count > 0:
        url = "{}/messages.getHistory".format(config.get("DOMAIN"))
        response = get(url, params=query_params)
        count -= min(count, max_count)
        query_params['offset'] += 200
        query_params['count'] = min(count, max_count)
        messages += response.json()['response']['items']
        time.sleep(0.333333334)

    return messages
