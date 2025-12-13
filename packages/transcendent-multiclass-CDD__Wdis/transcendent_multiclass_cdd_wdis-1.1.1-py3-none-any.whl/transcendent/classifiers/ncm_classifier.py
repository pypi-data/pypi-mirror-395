from abc import abstractmethod, ABC

from transcendent import data
import os


def load_model(model_filename):
    if model_filename and os.path.exists(model_filename):
        model = data.load_cached_data(model_filename)
        return model
    return None


class NCMClassifier(ABC):
    def ncm(self):
        raise NotImplementedError()
