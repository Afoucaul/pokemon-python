import tkinter as tk

from core.overworld import Overworld
from core.tileset import Tileset

if __name__ == '__main__':
    import map_frame
else:
    from . import map_frame


class SingletonError(Exception):
    pass


class App(tk.Tk):
    instance = None

    def __init__(self):
        if self.instance is not None:
            raise SingletonError
        else:
            self.instance = self

        self.tileset = None
        self.overworld = None

        self.mapFrame = map_frame.MapFrame(self)
        self.mapFrame.pack()

    def load_tileset(self, path):
        self.tileset = Tileset.load(path)
        self.mapFrame.draw()

    def load_overworld(self, path):
        self.overworld = Overworld.load(path)
        self.mapFrame.draw()


if __name__ == '__main__':
    App().run()
