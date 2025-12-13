import os
import numpy as np
from transcendent import data
from transcendent.classifiers.ncm_classifier import *
import lightgbm as lgb


class LGBWMarginNCM(NCMClassifier):
    def __init__(self, **kwargs):
        super().__init__()
        self.model_filename = kwargs.pop("model_filename", None)
        self.params = kwargs
        self.model = None
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

    def ncm(self, X, y):
        # Get raw scores (margins) for all classes
        raw_scores = self.model.predict(
            X, raw_score=True
        )  # shape=(n_samples, n_classes)
        # raw_scores = self.model.decision_function(X)

        ncm = []
        for i in range(len(X)):
            sample_scores = raw_scores[i]
            top_score = sample_scores[y[i]]

            # Mask predicted class and get max of remaining
            other_scores = np.delete(sample_scores, y[i])
            second_score = np.max(other_scores)

            # Margin = difference between top and second score
            margin = top_score - second_score
            ncm.append(-margin)  # Negative because high margin = low nonconformity

        return np.array(ncm)

    def predict(self, X):
        probs = self.model.predict(X)
        return probs.argmax(axis=1)
