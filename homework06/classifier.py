from collections import Counter
from pprint import pprint as pp
from math import log1p


class NaiveBayesClassifier:
    
    def __init__(self, alpha=1.0):
        self.alpha = alpha

    def fit(self, X, y):
        """ Fit Naive Bayes classifier according to X, y. """
        counted_words = dict(Counter(self._get_normalized_words(X)))
        counted_classes = dict(Counter(y))
        appearance_by_class = self._count_appearances(X, y)

        ALPHA = self.alpha
        D = len(counted_words)
        model = {
            'likelihood': {},
            'classes': []
        }

        for clss in counted_classes:
            model['classes'].append((clss, counted_classes[clss] / len(y)))

        for word in counted_words:
            params = {}

            for clss in counted_classes:
                Nc = counted_words.get(word, 0)
                Nic = appearance_by_class.get((word, clss), 0)

                params[clss] = (Nic + ALPHA) / (Nc + ALPHA * D)

            model['likelihood'][word] = params
                
        self.model = model

    def predict(self, X):
        """ Perform classification on an array of test vectors X. """
        answers_lst = []

        for sentence in X:
            words = self._get_normalized_words(sentence.split())
            answer, answer_score = '', -100000000

            for clss, prior_value in self.model['classes']:
                total_score = log1p(prior_value - 1)

                for word in words:
                    word_params = self.model['likelihood'].get(word, None)
                    
                    if word_params:
                        total_score += log1p(word_params[clss] - 1)

                if total_score > answer_score:
                    answer, answer_score = clss, total_score

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


    def _normalize_string(self, string):
        litter = ['.', ',', '!', '"', '\'', ':', ' -']
        clear_string = string.lower()

        for symbol in litter:
            clear_string = clear_string.replace(symbol, '')

        return clear_string

    def _get_normalized_words(self, X):
        words = []

        for sentence in X:
            clear_sentence = sentence.lower()
            clear_sentence = self._normalize_string(clear_sentence)

            words += clear_sentence.split()

        return words

    def _count_appearances(self, X, y):
        lst = []

        for sentence, clss in zip(X, y):
            sentence = self._normalize_string(sentence)
            for word in sentence.split():
                lst.append((word, clss))

        return Counter(lst)
