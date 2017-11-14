import requests
import datetime
from vk_api import get_friends
from pprint import pprint as pp


def filter(arr):
    new_arr = []
    for item in arr:
        if (item and len(item.split('.')) == 3):
            new_arr.append(item)
    return new_arr


def age_predict(user_id):
    """
    >>> age_predict(???)
    ???
    """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"

    response = get_friends(user_id, 'bdate')
    bdates = [c.get('bdate') for c in response.get('response').get('items')]
    bdates = filter(bdates)

    current_date = datetime.date.today()
    counter = 0
    for item in bdates:
        bdate_params = list(reversed(item.split('.')))
        bdate = datetime.date(int(bdate_params[0]),
                              int(bdate_params[1]),
                              int(bdate_params[2]))
        diff = current_date - bdate
        counter += diff.total_seconds() // (60 * 60 * 24 * 365)
    return counter // len(bdates)

if __name__ == '__main__':
    predicted_age = age_predict(145458606)
    print(predicted_age)
