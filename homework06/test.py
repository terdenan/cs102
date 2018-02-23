import csv
import string
from classifier import NaiveBayesClassifier

with open("SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))


def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)


def normalize_string(string):
        litter = ['.', ',', '!', '"', '\'', ':', ' -', ' —', '(', ')']
        clear_string = string.lower()

        for symbol in litter:
            clear_string = clear_string.replace(symbol, '')

        return clear_string


X, y = [], []

for target, msg in data:
    X.append(msg)
    y.append(target)

X = [normalize_string(x) for x in X]
X_train, y_train, X_test, y_test = X[:3900], y[:3900], X[3900:], y[3900:]

model = NaiveBayesClassifier(1)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))
