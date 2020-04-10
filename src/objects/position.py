from __future__ import annotations

from typing import List

from ..utils import SIZE
from .move import MOVE_TO_DELTA, Move


class Position:
    def __init__(self, pos):
        if pos not in range(SIZE ** 2):
            raise ValueError
        self.pos = pos

    def __str__(self):
        return f"Position {self.pos}"

    def __repr__(self):
        return f"Position {self.pos}"

    def __eq__(self, other):
        return self.pos == other.pos

    def get_adjacent_positions(self) -> List[Position]:
        moves = list(map(lambda x: self.pos + MOVE_TO_DELTA[x], Move))
        moves_in_borders = [Position(moves[0] % (SIZE ** 2)), Position(moves[1] % (SIZE ** 2))]

        if moves[2] % SIZE == (SIZE - 1):
            moves_in_borders.append(Position(moves[2] + SIZE))
        else:
            moves_in_borders.append(Position(moves[2]))

        if moves[3] % SIZE == 0:
            moves_in_borders.append(Position(moves[3] - SIZE))
        else:
            moves_in_borders.append(Position(moves[3]))

        return moves_in_borders
