import pygame
from . import picklable


class Tileset(picklable.Picklable):
    def __init__(self, image: pygame.Surface, tileSize):
        self.image = image
        self.tileSize = tileSize
        self.width, self.height = self.image.get_size()
        self.columnsCount = self.width / self.tileSize

    def _get_tile(self, index):
        row = index % self.columnsCount
        column = index // self.columnsCount

        rectangle = (-row * self.tileSize, -column * self.tileSize)
        tile = pygame.Surface((self.tileSize, self.tileSize), pygame.SRCALPHA)
        tile.blit(self.image, rectangle)

        return tile.convert_alpha()

    def __getitem__(self, index):
        return self._get_tile(index)
