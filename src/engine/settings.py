from core.picklable import Picklable


class Settings(Picklable):
    instance = None
    fields = {
        'APP_FPS': int,
        'START_MAP': str,
        'SCREEN_WIDTH': int,
        'SCREEN_HEIGHT': int,
        'SCALE': int}

    @classmethod
    def load(cls, path, options=0):
        instance = Picklable.load(path, options)
        cls.instance = instance
        return instance

    def __setattr__(self, name, value):
        if name in self.fields:
            super().__setattr__(name, self.fields[name](value))

    @classmethod
    def set(cls, name, value):
        if cls.instance is not None:
            setattr(cls.instance, value)
