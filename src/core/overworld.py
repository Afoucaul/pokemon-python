import numpy as np
from . import picklable
from .utils import BinaryEnum


class CollisionMask(BinaryEnum):
    WALKABLE    = 1
    SWIMMABLE   = 2
    BIKABLE     = 4


class Overworld(picklable.Picklable):
    def __init__(self, height, width):
        self.lowerTiles = np.zeros((height, width))
        self.upperTiles = - np.ones((height, width))
        self.collisions = - np.ones((height, width))

    @property
    def size(self):
        return self.lowerTiles.shape
