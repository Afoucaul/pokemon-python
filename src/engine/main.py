import pygame

from settings import Settings
from environment import Environment
from controller import KeyboardController

from core.picklable import PicklableOptions
from core.overworld import Overworld

from overworld.overworld_manager import OverworldManager
from overworld.tileset import PygameTileset


class App:
    def __init__(self, settingsPath="setup1.settings", scale=1):
        self.controller = KeyboardController()
        self.scale = scale

        Settings.load(settingsPath, options=PicklableOptions.READONLY)

        self.window = pygame.display.set_mode(
            (Settings.instance.SCREEN_WIDTH*self.scale,
             Settings.instance.SCREEN_HEIGHT*self.scale))

        self.do_environment()

    def do_environment(self):
        Environment.scale = self.scale
        Environment.controller = self.controller
        Environment.window = self.window

    def run(self):
        overworld = Overworld.load("../../data/overworlds/map1.overworld")
        tileset = PygameTileset.load("tileset")
        OverworldManager(tileset, overworld).run()


if __name__ == '__main__':
    pygame.init()
    app = App()
    print(Environment.window)
    app.run()
