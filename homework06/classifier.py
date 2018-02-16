from collections import Counter
from pprint import pprint as pp
from math import log1p


class NaiveBayesClassifier:

    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        self.appearance_by_class = self.count_appearances(X, y)

        self.counted_words = dict(Counter(self.get_normalized_words(X)))
        self.counted_classes = dict(Counter(y))

        self.model = {
            'classes': {},
            'words': {},
        }

        for cur_class in self.counted_classes:
            params = {
                'count_by_class': self._count_words(cur_class),
                'aprior_value': self.counted_classes[cur_class] / len(y),
            }
            self.model['classes'][cur_class] = params

        for word in self.counted_words:
            params = {}

            for cur_class in self.counted_classes:
                params[cur_class] = self._calculate_likelihood(word, cur_class)

            self.model['words'][word] = params

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        answers_lst = []

        for sentence in X:
            words = self.get_normalized_words(sentence.split())
            possible_answers = []

            for cur_class in self.model['classes']:
                aprior_value = self.model['classes'][cur_class]['aprior_value']
                total_score = log1p(aprior_value - 1)

                for word in words:
                    word_params = self.model['words'].get(word, None)

                    if word_params:
                        total_score += log1p(word_params[cur_class] - 1)

                possible_answers.append((total_score, cur_class))

            _, answer = max(possible_answers)
            answers_lst.append(answer)

        return answers_lst

    def score(self, X_test, y_test):
        """ Returns the mean accuracy on the given test data and labels. """
        total_count = len(y_test)
        correct = 0
        for i, answer in enumerate(self.predict(X_test)):
            if answer == y_test[i]:
                correct += 1

        return correct / total_count

    def _calculate_likelihood(self, word, cur_class):
        Nc = self.model['classes'][cur_class]['count_by_class']
        Nic = self.appearance_by_class.get((word, cur_class), 0)
        d = len(self.counted_words)
        alpha = self.alpha

        return (Nic + alpha) / (Nc + alpha * d)

    def _count_words(self, cur_class):
        total_count = 0

        for word, class_name in self.appearance_by_class:
            if cur_class == class_name:
                total_count += self.appearance_by_class[(word, cur_class)]

        return total_count

    @classmethod
    def normalize_string(cls, string):
        litter = ['.', ',', '!', '"', '\'', ':', ' -']
        clear_string = string.lower()

        for symbol in litter:
            clear_string = clear_string.replace(symbol, '')

        return clear_string

    @classmethod
    def get_normalized_words(cls, X):
        words = []

        for sentence in X:
            clear_sentence = sentence.lower()
            clear_sentence = cls.normalize_string(clear_sentence)

            words += clear_sentence.split()

        return words

    @classmethod
    def count_appearances(cls, X, y):
        lst = []

        for sentence, clss in zip(X, y):
            sentence = cls.normalize_string(sentence)
            for word in sentence.split():
                lst.append((word, clss))

        return Counter(lst)
