from core.tileset import Tileset

from PIL import Image, ImageTk


class TkTileset(Tileset):
    def __init__(self, imagePath, tileSize):
        super().__init__(imagePath, tileSize)
        self.tileHeight = tileSize
        self.tileWidth = tileSize
        self._prepare_tiles()

    def resize(self, tileWidth, tileHeight=None):
        self.tileWidth = tileWidth
        if tileHeight is None:
            self.tileHeight = self.tileWidth
        else:
            self.tileHeight = tileHeight

    def _prepare_tiles(self):
        self._tiles = [self._get_tile(i*self.columnCount + j)
                       for i in range(self.rowCount)
                       for j in range(self.columnCount)]

    def _prepare_image(self, imagePath):
        self.image = Image.open(imagePath)
        self.width = self.image.width
        self.height = self.image.height

    def _get_tile(self, index):
        row = index % self.columnCount
        column = index // self.columnCount

        rectangle = (
            row * self.tileSize,
            column * self.tileSize,
            (row + 1) * self.tileSize,
            (column + 1) * self.tileSize)
        tile = self.image.crop(rectangle)
        tile = tile.resize((self.tileWidth, self.tileHeight))

        return tile

    def __getitem__(self, index):
        tile = self._get_tile(index)

        return tile
