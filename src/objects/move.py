from enum import Enum

from ..utils import SIZE


class Move(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


MOVE_TO_DELTA = {Move.NORTH: -SIZE, Move.SOUTH: SIZE, Move.EAST: -1, Move.WEST: 1}
