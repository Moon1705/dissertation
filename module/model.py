import json
import os
import pickle
import numpy
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn import svm
from sklearn.linear_model import LogisticRegression, SGDClassifier
from sklearn.neural_network import MLPClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import NearestCentroid
from data.create_data import create_data


class Model:

    def __init__(self, model_path='data/model.pkl', create_model=True):
        if not os.path.isfile(model_path) or create_model:
            self.create_model(save_model_path=model_path)
        self.model = self.load_model(load_model_path=model_path)

    def __create_labels(self, labels):
        encoder = LabelEncoder()
        encoder.fit(labels)
        return encoder.transform(labels)

    def __load_data(self, load_data_path):
        # if not os.path.isfile(load_data_path): create_data(load_data_path)
        create_data(load_data_path)
        with open(load_data_path, 'r', encoding='utf-8') as file:
            return numpy.array(list(map(lambda x: list(x.values()), json.load(file))))

    def __create_classifiers(self, train_events, train_labels):
        classifiers = []
        classifiers.append(svm.SVC(kernel='poly'))
        classifiers.append(LogisticRegression(solver='sag', random_state=42))
        classifiers.append(MLPClassifier(solver='lbfgs', hidden_layer_sizes=(5,3), max_iter=1000, random_state=42))
        classifiers.append(GaussianNB())
        classifiers.append(SGDClassifier(random_state=42))
        classifiers.append(DecisionTreeClassifier(criterion='gini', splitter='best', random_state=42))
        classifiers.append(NearestCentroid())
        for classifier in classifiers:
            classifier.fit(train_events, train_labels)
        return classifiers

    def __choice_best_classifiers(self, classifiers, test_events, test_labels):
        max_value = 0
        best_classifier = object()
        for classifier in classifiers:
            value = classifier.score(test_events, test_labels)
            if value > max_value:
                max_value = value
                best_classifier = classifier
        return best_classifier

    def create_model(self, load_data_path='data/dataset.json', save_model_path='data/model.pkl'):
        data = self.__load_data(load_data_path)
        train_events, test_events, train_labels, test_labels = train_test_split(data[:, 1:].astype(float), self.__create_labels(data[:, 0].astype(str)), test_size=0.2, random_state=42)
        classifiers = self.__create_classifiers(train_events, train_labels)
        best_classifier = self.__choice_best_classifiers(classifiers, test_events, test_labels)
        pickle.dump(best_classifier, open(save_model_path, 'wb'))

    def load_model(self, load_model_path='data/model.pkl'):
        return pickle.load(open(load_model_path, 'rb'))

    def check_event(self, event):
        return self.model.predict(numpy.array([event]).astype(float))[0]