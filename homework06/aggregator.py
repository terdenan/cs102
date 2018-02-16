import requests
from bs4 import BeautifulSoup
from pprint import pprint as pp
import sqlalchemy


def get_news(url='https://news.ycombinator.com/news', n_pages=1):
    news = []
    for i in range(1, n_pages + 1):
        query = f"{url}?p={i}"
        r = requests.get(query)
        page = BeautifulSoup(r.text, 'html.parser')
        news += extract_news(page)

    return news
        

def extract_news(page):
    news = []
    itemlist = page.find('table', {'class': 'itemlist'})
    trs = itemlist.findAll('tr')

    news_description = trs[:90:3]
    news_stats = trs[1:90:3]

    for single_news in zip(news_description, news_stats):
        dscrpt, stats = single_news

        author = stats.find('a', {'class': 'hnuser'})
        points = stats.find('span', {'class': 'score'})
        comments = stats.findAll('a')[-1].next.split()

        news.append({
            'id': int(dscrpt['id']),
            'author': author.next if author else None,
            'comments': comments[0] if len(comments) == 2 else None,
            'points': int(points.next.split()[0]) if points else None,
            'title': dscrpt.find('a', {'class': 'storylink'}).next,
            'url': dscrpt.find('a', {'class': 'storylink'})['href'],
            })

    return news


def extract_next_page():
    pass


news = get_news('https://news.ycombinator.com/news', n_pages=1)
pp(news)
