import pickle


class PicklableError(Exception):
    pass


class Picklable:
    @classmethod
    def load(cls, path):
        with open(path, 'rb') as source:
            obj = pickle.load(source)

        if isinstance(obj, cls):
            return obj
        else:
            raise PicklableError("Tried to unpickle a {} instance,"
                                 "but found a {} instance".format(
                                     cls.__name__,
                                     type(obj).__name__))

    @classmethod
    def save(cls, path, obj):
        if isinstance(obj, cls):
            with open(path, 'wb') as target:
                pickle.dump(target, obj)
        else:
            raise PicklableError("Tried to pickle a {} instance,"
                                 "but found a {} instance".format(
                                     cls.__name__,
                                     type(obj).__name__))
