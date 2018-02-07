import pickle


class Picklable:
    def __init__(self):
        self.picklePath = None

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as source:
            obj = pickle.load(source)
            obj.picklePath = path
            return obj

    def dump(self, path=None):
        if path is None:
            path = self.picklePath

        with open(path, 'wb') as target:
            pickle.dump(self, target)
