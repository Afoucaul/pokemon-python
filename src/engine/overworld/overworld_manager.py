import numpy as np
import pygame
from pygame.locals import QUIT

from settings import Settings
from environment import Environment


class OverworldManager:
    def __init__(self, tileset, overworld):
        self.tileset = tileset
        self.overworld = overworld

        self.surface = pygame.Surface(
            (self.overworld.shape[0] * self.tileset.tileSize,
             self.overworld.shape[1] * self.tileset.tileSize))
        self.running = False

    def draw_overworld(self):
        self.surface.blit(self.tileset[self.overworld.lowerTiles[0, 0]], (0, 0))
        for layer in self.overworld.layers:
            it = np.nditer(layer, flags=['multi_index'])
            while not it.finished:
                tileId = int(it[0])
                if tileId != -1:
                    tile = self.tileset[tileId]
                    x, y = it.multi_index
                    x *= self.tileset.tileSize
                    y *= self.tileset.tileSize

                    self.surface.blit(tile, (x, y))
                it.iternext()

        Environment.window.blit(self.surface, ((0, 0)))

    def run(self):
        controller = Environment.controller
        clock = pygame.time.Clock()
        self.running = True
        while self.running:
            clock.tick(Settings.instance.APP_FPS)

            for event in pygame.event.get():
                if event.type == QUIT:
                    self.running = False

                controller.process(event)

            self.draw_overworld()
            pygame.display.flip()
