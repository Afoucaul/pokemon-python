import tkinter as tk

from core.overworld import Overworld
from core.picklable import PicklableOptions

import map_frame
import tileset_frame
import main_menu
import collision_frame
from tileset import TkTileset


class SingletonError(Exception):
    pass


class App(tk.Tk):
    instance = None

    def __init__(self):
        if type(self).instance is not None:
            raise SingletonError
        else:
            type(self).instance = self

        super().__init__()

        self.tileset = None
        self.overworld = None

        self.mapFrame = map_frame.MapFrame(self)
        self.tilesetFrame = tileset_frame.TilesetFrame(self)
        self.mainMenu = main_menu.MainMenu(self)
        self.collisionFrame = collision_frame.CollisionFrame(self)

        self.mapFrame.pack(fill=tk.BOTH, expand=True, side=tk.LEFT)
        self.tilesetFrame.pack(fill=tk.Y, side=tk.LEFT)
        self.collisionFrame.pack(expand=True, fill=tk.Y, side=tk.LEFT)
        self.config(menu=self.mainMenu)

        self.resizable(False, True)
        self.minsize(250, 800)

    def load_tileset(self, path):
        print("Loading tileset from {}...".format(path))
        self.tileset = TkTileset.load(path, PicklableOptions.READONLY)
        self.mapFrame.draw()
        self.tilesetFrame.draw()
        print("Tileset loaded.")

    def load_overworld(self, path):
        print("Loading map from {}...".format(path))
        self.overworld = Overworld.load(path)
        self.mapFrame.clear()
        self.mapFrame.draw()
        self.mapFrame.radiobuttons.reset()
        self.title(path.rsplit("/", 1)[-1])
        print("Map loaded.")

    def save_overworld(self, path=None):
        print("Saving map...")
        self.overworld.dump(path)
        print("Map saved.")

    def close_overworld(self):
        self.mapFrame.clear()
        self.overworld = None

    def run(self):
        self.mainloop()
