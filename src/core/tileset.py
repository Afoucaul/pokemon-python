import pygame

from .picklable import Picklable


class Tileset(Picklable):
    def __init__(self, imagePath, tileSize):
        self._prepare_image(imagePath)
        self.tileSize = tileSize
        self.columnCount = self.width // self.tileSize
        self.rowCount = self.height // self.tileSize

    def __getitem__(self, index):
        return self._get_tile(index)


class PygameTileset(Tileset):
    def _prepare_image(self, imagePath):
        self.image = pygame.image.load(imagePath)
        self.height = self.image.get_height()

    def _get_tile(self, index):
        row = index % self.columnCount
        column = index // self.columnCount

        rectangle = (-row * self.tileSize, -column * self.tileSize)
        tile = pygame.Surface((self.tileSize, self.tileSize), pygame.SRCALPHA)
        tile.blit(self.image, rectangle)

        return tile.convert_alpha()
