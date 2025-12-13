import numpy as np
from sklearn.ensemble import RandomForestClassifier
from transcendent import data
from transcendent.classifiers.ncm_classifier import NCMClassifier
import os


class RandomForestWProbNCM(NCMClassifier):
    def __init__(self, **kwargs):
        NCMClassifier.__init__(self)
        self.model_filename = kwargs.pop("model_filename", None)
        self.model = (
            RandomForestClassifier(**kwargs)
            if not os.path.exists(self.model_filename)
            else data.load_cached_data(self.model_filename)
        )

    def fit(self, X_train, y_train):
        if os.path.exists(self.model_filename):
            self.model = data.load_cached_data(self.model_filename)
        else:
            self.model.fit(X_train, y_train)
        data.cache_data(self.model, self.model_filename)

    def predict(self, X):
        return self.model.predict(X)

    def ncm(self, X, y):
        probas = self.model.predict_proba(X)
        return 1 - probas[np.arange(len(y)), y]
