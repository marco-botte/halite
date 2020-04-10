import logging
from enum import Enum
from random import choice

logger = logging.getLogger()  # pylint: disable = C0103

SIZE = 15


class Move(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"
    NONE = None


MOVE_TO_DELTA = {Move.NORTH: -SIZE, Move.SOUTH: SIZE, Move.EAST: -1, Move.WEST: 1, Move.NONE: 0}


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

    def get_adjacent_positions(self):
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

        return moves_in_borders + [self]


def first_agent(obs):
    # logger.warning(obs.players[0])

    action_dict = {}

    shipyard_id_list = list(obs.players[obs.player][1].keys())
    ship_id_list = list(obs.players[obs.player][2].keys())

    if obs.players[obs.player][0] > 4000 and ship_id_list:
        action_dict[ship_id_list[0]] = "CONVERT"

    elif obs.players[obs.player][0] >= 1000 and obs.step % 4 == 1 and shipyard_id_list:
        action_dict[shipyard_id_list[0]] = "SPAWN"

    else:
        ship_action = choice(list(Move)).value
        if ship_action is not None:
            action_dict[ship_id_list[0]] = ship_action
    # logger.warning(f"Action:\t {action_dict}")  # pylint: disable = W1202
    return action_dict
