from __future__ import annotations
from enum import Enum, auto


class Dir(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    

class GridVector:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y

    def copy(self) -> GridVector:
        return GridVector(self.x, self.y)

    def __eq__(self, other: GridVector) -> bool:
        return self.x == other.x and self.y == other.y

    def __str__(self) -> str:
        return "GridVector({}, {})".format(self.x, self.y)
