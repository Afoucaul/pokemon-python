from core.tileset import Tileset

from PIL import Image, ImageTk


class TkTileset:
    def __init__(self, tileset: Tileset):
        self.tileset = tileset
        self.image = Image.open(self.tileset.imagePath)
        self.width = self.tileset.image.width
        self.height = self.tileset.image.height
        self.columnCount = self.width // self.tileset.tileSize
        self.rowCount = self.height // self.tileset.tileSize

    def get_tile(self, index, size):
        row = index % self.columnCount
        column = index // self.columnCount

        rectangle = (
            row * self.tileset.tileSize,
            column * self.tileset.tileSize,
            (row + 1) * self.tileset.tileSize,
            (column + 1) * self.tileset.tileSize)
        tile = self.image.crop(rectangle)
        tile = tile.resize((size, size))

        return tile

    def get_tiles(self, size):
        return [ImageTk.PhotoImage(self.get_tile(i*self.rowCount + j, size))
                for i in range(self.rowCount)
                for j in range(self.columnCount)]
