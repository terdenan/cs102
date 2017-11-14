import requests
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import datetime
from vk_api import get_messages_history
from pprint import pprint as pp


def count_dates_from_messages(messages):
    def findAmountByDate(date):
        cnt = 0
        for item in messages:
            cur_date = datetime.fromtimestamp(item['date'])
            .strftime("%Y-%m-%d")
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
    messages = get_messages_history(223703977)
    x, y = count_dates_from_messages(messages)
    data = [go.Scatter(x=x, y=y)]
    py.plot(data)
