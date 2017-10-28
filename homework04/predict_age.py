import requests
import datetime
from pprint import pprint as pp


DOMAIN = "https://api.vk.com/method"
ACCESS_TOKEN = "9e2b793e5cb009775d94bd2d1bd375dd970d8dbb105b542c8e5\
626c55f07c5f2f05250ae3d0ee5d689695"


def get_friends(user_id, fields):
    """ Returns a list of user IDs or detailed\
    information about a user's friends """
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert isinstance(fields, str), "fields must be string"
    assert user_id > 0, "user_id must be positive integer"
    query_params = {
        'domain': DOMAIN,
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'fields': fields
    }
    query = "{domain}/friends.get?access_token={access_token}\
&user_id={user_id}&fields={fields}&v=5.53".format(**query_params)
    response = requests.get(query)
    return response.json()


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

