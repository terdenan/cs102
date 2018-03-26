from aggregator import get_news
from bottle import request, route, run, template, redirect
from classifier import NaiveBayesClassifier
from pprint import pprint as pp
from db import session, News, exists


@route('/news')
def news_list():
    rows = s.query(News).filter(News.label == None).all()
    return template('templates/news_template', rows=rows)


@route('/update_news')
def update_news():
    news = get_news('https://habrahabr.ru/all/top50', n_pages=1)
    for n in news:
        (is_exists, ), = s.query(exists().where(News.id == n.get('id')))
        if not is_exists:
            s.add(News(**n))
            s.commit()

    redirect('/news')


@route('/add_label')
def add_label():
    label, id = request.query['label'], request.query['id']
    s.query(News).filter(News.id == id).update({'label': label})
    s.commit()
    redirect('/news')


@route('/recommendations')
def recommendations():
    rows = s.query(News).filter(News.label == None).all()
    news = []
    for row in rows:
        [prediction] = model.predict([row.normal_title])
        if prediction == 'good':
            news.append(row)

    return template('templates/news_recommendations', rows=news)


def get_training_data():
    rows = s.query(News).filter(News.label != None).all()
    X_train = [row.normal_title for row in rows]
    y_train = [row.label for row in rows]

    return X_train, y_train


if __name__ == '__main__':
    s = session()
    X_train, y_train = get_training_data()
    model = NaiveBayesClassifier(1)
    model.fit(X_train, y_train)
    run(host='localhost', port=8080)

    # print(len(s.query(News).filter(News.label != None).all()))
    # cnt = 183
    # X, y = get_training_data()
    # X_train, y_train, X_test, y_test = X[:cnt], y[:cnt], X[cnt:], y[cnt:]
    # model = NaiveBayesClassifier(1)
    # model.fit(X_train, y_train)
    # print(model.score(X_test, y_test))
