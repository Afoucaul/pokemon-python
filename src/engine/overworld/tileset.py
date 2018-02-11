import pygame
import core.tileset


class PygameTileset(core.tileset.Tileset):
    def _prepare_image(self):
        pygame.init()
        pygame.display.set_mode((0, 0))
        self.image = pygame.image.load(self.imagePath).convert_alpha()
        self.height = self.image.get_height()
        self.width = self.image.get_width()

    def _get_tile(self, index):
        row = index % self.columnCount
        column = index // self.columnCount

        rectangle = (-row * self.tileSize, -column * self.tileSize)
        tile = pygame.Surface((self.tileSize, self.tileSize), pygame.SRCALPHA)
        tile.blit(self.image, rectangle)

        return tile.convert_alpha()
