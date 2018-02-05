import numpy as np
from . import picklable


class Overworld(picklable.Picklable):
    def __init__(self, height, width):
        self.lowerTiles = np.zeros((height, width))
        self.upperTiles = np.zeros((height, width))
        self.collisions = np.zeros((height, width))

    @property
    def size(self):
        return self.lowerTiles.shape
