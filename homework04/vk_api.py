import requests
from config import config
import time


def get(query, timeout=5, max_retries=5, backoff_factor=0.3):
    """ Выполнить GET-запрос

    :param query: тело GET запроса
    :param timeout: максимальное время ожидания ответа от сервера
    :param max_retries: максимальное число повторных запросов
    :param backoff_factor: коэффициент экспоненциального нарастания задержки
    """
    delay = 1
    response = {}
    while max_retries:
        try:
            response = requests.get(query, timeout=timeout)
            break
        except requests.exceptions.Timeout:
            print("Timeout exception")

        time.sleep(delay)
        max_retries -= 1
        delay *= (1.0 + backoff_factor)

    return response


def get_friends(user_id, fields=''):
    """ Returns a list of user IDs or detailed\
    information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': config.get("DOMAIN"),
        'access_token': config.get("ACCESS_TOKEN"),
        'user_id': user_id,
        'fields': fields
    }
    query = "{domain}/friends.get?access_token={access_token}\
&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = get(query)
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
        'count': min(count, max_count)
    }
    messages = []

    while count > 0:
        cur_count = min(count, max_count)
        query = "{domain}/messages.getHistory?access_token={access_token}\
&user_id={user_id}&count={count}&offset={offset}&v=5.53".format(**query_params)
        count -= cur_count
        query_params['offset'] += 200
        query_params[count] = min(count, max_count)
        response = get(query)
        messages += response.json()['response']['items']
        time.sleep(0.333333334)

    return messages
