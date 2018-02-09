import pickle

from .utils import BinaryEnum


class PicklableError(Exception):
    pass


class PicklableOptions(BinaryEnum):
    READONLY = 1


class Picklable:
    @classmethod
    def load(cls, path, options=0):
        with open(path, 'rb') as source:
            obj = pickle.load(source)
            obj.picklePath = path
            obj.options = options
            return obj

    def dump(self, path=None):
        try:
            options = PicklableOptions.get_options(self.options)
        except AttributeError:
            options = []

        if PicklableOptions.READONLY in options:
            raise PicklableError("Cannot dump read-only instance of {}".format(
                type(self).__name__))

        if path is None:
            path = self.picklePath

        with open(path, 'wb') as target:
            pickle.dump(self, target)
