import requests
from datetime import datetime
from pprint import pprint as pp
import plotly.plotly as py
import plotly.graph_objs as go


DOMAIN = "https://api.vk.com/method"
ACCESS_TOKEN = "9e2b793e5cb009775d94bd2d1bd375dd970d8dbb105b542c8e5\
626c55f07c5f2f05250ae3d0ee5d689695"

def messages_get_history(user_id, offset=0, count=200):
    assert isinstance(user_id, int), "user_id must be positive integer"
    assert user_id > 0, "user_id must be positive integer"
    assert isinstance(offset, int), "offset must be positive integer"
    assert offset >= 0, "user_id must be positive integer"
    assert count >= 0, "user_id must be positive integer"
    query_params = {
        'domain': DOMAIN,
        'access_token': ACCESS_TOKEN,
        'user_id': user_id,
        'offset': offset,
        'count': count
    }
    messages = []

    query = "{domain}/messages.getHistory?access_token={access_token}\
&user_id={user_id}&count={count}&offset={offset}&v=5.53".format(**query_params)
    response = requests.get(query)
    messages += response.json()['response']['items']
    query_params['offset'] = 200

    query = "{domain}/messages.getHistory?access_token={access_token}\
&user_id={user_id}&count={count}&offset={offset}&v=5.53".format(**query_params)
    response = requests.get(query)
    messages += response.json()['response']['items']
    query_params['offset'] = 400

    query = "{domain}/messages.getHistory?access_token={access_token}\
&user_id={user_id}&count={count}&offset={offset}&v=5.53".format(**query_params)
    response = requests.get(query)
    messages += response.json()['response']['items']

    return messages


def count_dates_from_messages(messages):
    def findAmountByDate(date):
        cnt = 0
        for item in messages:
            cur_date = datetime.fromtimestamp(item['date']).strftime("%Y-%m-%d")
            if (date == cur_date):
                cnt += 1

        return cnt

    x = []
    y = []
    for item in messages:
        cur_date = datetime.fromtimestamp(item['date']).strftime("%Y-%m-%d")
        if (cur_date in x):
            continue
        x.append(cur_date)
        y.append(findAmountByDate(cur_date))

    return (x, y)


if __name__ == '__main__':
    messages = messages_get_history(223703977)
    x, y = count_dates_from_messages(messages)
    data = [go.Scatter(x=x, y=y)]
    py.plot(data)
