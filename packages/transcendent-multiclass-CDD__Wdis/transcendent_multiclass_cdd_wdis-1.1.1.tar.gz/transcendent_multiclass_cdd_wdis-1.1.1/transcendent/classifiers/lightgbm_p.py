import os
import numpy as np
from transcendent import data
from transcendent.classifiers.ncm_classifier import *
import lightgbm as lgb


class LGBWProbNCM(NCMClassifier):
    def __init__(self, **kwargs):
        super().__init__()
        self.model_filename = kwargs.pop("model_filename", None)
        self.params = kwargs
        self.model = load_model(self.model_filename)

    def fit(self, X_train, y_train):
        self.model = load_model(self.model_filename)
        if self.model is None:
            dtrain = lgb.Dataset(X_train, label=y_train)
            self.model = lgb.train(
                params=self.params,
                train_set=dtrain,
                # callbacks=[lgb.early_stopping(stopping_rounds=50)],
            )
            # self.model = lgb.LGBMClassifier(**self.params)
            # self.model.fit(X_train, y_train)
            data.cache_data(self.model, self.model_filename)

    def predict(self, X):
        probs = self.model.predict(X)
        return probs.argmax(axis=1)

    def ncm(self, X, y):
        # Predict all probabilities at once (shape: [n_samples, n_classes])
        probas = self.model.predict(X)

        # Vectorized extraction of correct class probabilities
        # (1 - probability of the true class for each calibration example)
        return 1 - probas[np.arange(len(y)), y]
