import requests
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from vk_api import get_messages_history
from pprint import pprint as pp
from collections import Counter


def count_dates_from_messages(messages):
    def parse(d):
        return datetime.fromtimestamp(d).strftime("%Y-%m-%d")

    msg_list = [parse(c.get('date')) for c in messages]
    counted = Counter(msg_list)

    x = []
    y = []
    for key in counted:
        x.append(key)
        y.append(counted[key])

    return x, y


if __name__ == '__main__':
    messages = get_messages_history(223703977)
    x, y = count_dates_from_messages(messages)
    data = [go.Scatter(x=x, y=y)]
    py.plot(data)
