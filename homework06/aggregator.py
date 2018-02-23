import requests
import sqlalchemy
import pymorphy2
import time
from bs4 import BeautifulSoup
from pprint import pprint as pp

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


Base = declarative_base()
engine = create_engine("sqlite:///news.db")
session = sessionmaker(bind=engine)


class News(Base):
    __tablename__ = "news"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    normal_title = Column(String)
    author = Column(String)
    url = Column(String)
    comments = Column(Integer)
    points = Column(Integer)
    label = Column(String)


Base.metadata.create_all(bind=engine)

morph = pymorphy2.MorphAnalyzer()


def get_news(url='https://habrahabr.ru/all/top50', n_pages=1):
    news = []
    n_pages = min(n_pages, 100)

    for i in range(1, n_pages + 1):
        query = f"{url}/page{i}"
        r = requests.get(query)
        page = BeautifulSoup(r.text, 'html.parser')
        news += extract_news(page)

    return news


def extract_news(page):
    news = []

    contentlist = page.find('ul', {'class': 'content-list'})
    posts = contentlist.findAll('li', {'class': 'content-list__item'})

    for post in posts:

        if not post.get('id'):
            continue

        author = post.find('span', {'class': 'user-info__nickname'})
        comments = post.find('span', {'class', 'post-stats__comments-count'})
        points = post.find('span', {'class', 'voting-wjt__counter'})
        title = post.find('a', {'class': 'post__title_link'}).next
        normal_title = normalize(title)

        news.append({
            'id': post.get('id').split('_')[1],
            'author': author.next if author else None,
            'comments': comments.next if comments else 0,
            'points': int(points.next) if points else 0,
            'title': title,
            'normal_title': normal_title,
            'url': post.find('a', {'class': 'post__title_link'}).get('href'),
        })

    return news


def extract_next_page():
    pass


def normalize(string):
        litter = ['.', ',', '!', '"', '\'', ':', ' -', ' —', '(', ')', '?']
        clear_string = string.lower()
        normalized_words = []

        for symbol in litter:
            clear_string = clear_string.replace(symbol, '')

        for word in clear_string.split():
            # WARNING: Неоптимальный выбор нормальной формы
            normalized_words.append(morph.parse(word)[0].normal_form)

        return ' '.join(normalized_words)
