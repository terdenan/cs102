import csv
import string
from classifier import NaiveBayesClassifier

with open("SMSSpamCollection") as f:
    data = list(csv.reader(f, delimiter="\t"))

def clean(s):
    translator = str.maketrans("", "", string.punctuation)
    return s.translate(translator)

X, y = [], []

for target, msg in data:
    X.append(msg)
    y.append(target)

X = [clean(x).lower() for x in X]
cnt = 3900
X_train, y_train, X_test, y_test = X[:cnt], y[:cnt], X[cnt:], y[cnt:]

model = NaiveBayesClassifier(0.000000001)
model.fit(X_train, y_train)
print(model.score(X_test, y_test))