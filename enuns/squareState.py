from enum import Enum

class SquareState(Enum):
    Empty = 0,
    Black = 1,
    White = 2,
    Highlighted = 3,
    Highlighted_Black = 4,
    Highlighted_White = 5