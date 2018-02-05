import pickle


class PicklableError(Exception):
    pass


class Picklable:
    def __init__(self):
        self.picklePath = None

    @classmethod
    def load(cls, path):
        with open(path, 'rb') as source:
            obj = pickle.load(source)

        if isinstance(obj, cls):
            obj.picklePath = path
            return obj
        else:
            raise PicklableError("Tried to unpickle a {} instance,"
                                 "but found a {} instance".format(
                                     cls.__name__,
                                     type(obj).__name__))

    def dump(self, path=None):
        if path is None:
            path = self.picklePath

        with open(path, 'wb') as target:
            pickle.dump(target, self)
