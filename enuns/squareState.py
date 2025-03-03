from enum import Enum

class SquareState(Enum):
    Empty = 0,
    Black = 1,
    White = 2,
    Selected = 3,
    Selected_Black = 4,
    Selected_White = 5