import logging
from enum import Enum
from random import choice, random

import numpy as np

logger = logging.getLogger()  # pylint: disable = C0103

SIZE = 15
MOVE_PROB = 0.66


class Move(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


def board_pos_to_position(pos):
    return Position(pos // SIZE, pos % SIZE)


class Position:
    def __init__(self, x, y):
        self.x = x  # pylint: disable=C0103
        self.y = y  # pylint: disable=C0103

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_adjacent_position(self, move):
        if move == Move.NORTH:
            return Position((self.x - 1) % SIZE, self.y)
        if move == Move.SOUTH:
            return Position((self.x + 1) % SIZE, self.y)
        if move == Move.EAST:
            return Position(self.x, (self.y + 1) % SIZE)
        if move == Move.WEST:
            return Position(self.x, (self.y - 1) % SIZE)
        raise TypeError

    def get_all_adjacent_positions(self):
        return list(map(self.get_adjacent_position, Move))


class Ship:
    def __init__(self, name, pos):
        self.pos = pos
        self.name = name
        self.task_queue = None
        self.halite = 0

    def move(self, move):
        self.pos = self.pos.get_adjacent_position(move)
        self.halite *= 0.9

    def collect(self, board):
        self.halite += 0.25 * board[self.pos.x][self.pos.y]

    def set_tasks(self, queue):
        self.task_queue = queue

    def __str__(self):
        return (
            f"Ship(name={self.name}, pos={self.pos}, task={self.task_queue}, halite={self.halite}"
        )

    def __repr__(self):
        return (
            f"Ship(name={self.name}, pos={self.pos}, task={self.task_queue}, halite={self.halite}"
        )

    def __eq__(self, other):
        return self.name == other.name


class Shipyard:
    def __init__(self, name, pos):
        self.pos = pos
        self.name = name
        self.occupied = False

    def __str__(self):
        return f"Shipyard(name={self.name}, pos={self.pos}, occupied={self.occupied})"

    def __repr__(self):
        return f"Shipyard(name={self.name}, pos={self.pos}, occupied={self.occupied}"

    def __eq__(self, other):
        return self.pos == other.pos

    def set_occupied(self):
        self.occupied = True

    def set_unoccupied(self):
        self.occupied = False


class Player:
    def __init__(self):
        self.step = 0
        self.ships = dict()
        self.halite = 5000
        self.shipyards = dict()

    def add_shipyard(self, name, pos):
        self.shipyards[name] = Shipyard(name, pos)
        print(name, pos)
        print(self.shipyards)
        self.halite -= 2000

    def add_ship(self, name, pos):
        self.ships[name] = Ship(name, pos)
        self.halite -= 500

    def remove_ship(self, name):
        if self.ships.get(name) is not None:
            del self.ships[name]
        else:
            raise KeyError

    def convert_ship(self, ship_name, yard_name):
        if self.ships.get(ship_name) is not None:
            self.add_shipyard(yard_name, self.ships[ship_name].pos)
            self.remove_ship(ship_name)
        else:
            raise KeyError

    def spawn_ship(self, yard_name, ship_name):
        if self.shipyards.get(yard_name) is not None:
            shipyard = self.shipyards[yard_name]
            self.add_ship(ship_name, shipyard.pos)
            shipyard.set_occupied()
        else:
            raise KeyError

    def all_ship_positions(self):
        return list(map(lambda x: (x.name, x.pos), self.ships.values()))

    def crash_test(self):
        occupied = self.all_ship_positions()
        if len(set(occupied)) < len(occupied):
            return True
        return False


PLAYER = Player()


def initialize(obs):
    shipyards = obs.players[obs.player][1]
    for name, board_pos in shipyards.items():
        PLAYER.add_shipyard(name, board_pos_to_position(board_pos))

    ships = obs.players[obs.player][2]
    for name, props in ships.items():
        PLAYER.add_ship(name, board_pos_to_position(props[0]))
    logger.warning("Initialize finished")


def first_agent(obs):
    logger.warning(f"step {obs.step}, player {obs.players[0]}")
    action_dict = {}
    owned_halite = obs.players[obs.player][0]
    board = np.reshape(np.float32(obs.halite), (15, 15))
    action_counter = 1
    new_ship_names = set()
    new_shipyard_names = set()

    if PLAYER.step == 0:
        initialize(obs)

    for shipyard in PLAYER.shipyards.values():
        logger.warning(shipyard)
    for ship in PLAYER.ships.values():
        logger.warning(ship)

    # convert random ship to shipyard
    if PLAYER.ships and owned_halite > 4000:
        converted_ship_name = choice(list(PLAYER.ships))
        shipyard_name = f"{PLAYER.step+1}-{action_counter}"
        new_shipyard_names.add(shipyard_name)
        PLAYER.convert_ship(converted_ship_name, shipyard_name)
        action_dict[converted_ship_name] = "CONVERT"
        owned_halite -= 2000
        action_counter += 1

    # spawn ship in random shipyard when no ship available
    old_shipyards = list(filter(lambda x: x not in new_shipyard_names, PLAYER.shipyards))
    if old_shipyards and owned_halite >= 500 and len(PLAYER.ships) == 0:
        spawning_shipyard_name = choice(list(old_shipyards))
        ship_name = f"{PLAYER.step+1}-{action_counter}"
        new_ship_names.add(ship_name)
        PLAYER.spawn_ship(spawning_shipyard_name, ship_name)
        action_dict[spawning_shipyard_name] = "SPAWN"
        owned_halite -= 500
        action_counter += 1

    # choose action for each ship
    for ship_name, ship in PLAYER.ships.items():
        if ship_name in new_ship_names:
            continue

        if random() < MOVE_PROB:  # move ship
            ship_move = choice(list(Move))
            action_dict[ship_name] = ship_move.value
            ship.move(ship_move)
        else:  # collect
            ship.collect(board)

    logger.warning(f"Actions:\t {action_dict}")  # pylint: disable = W1202
    PLAYER.step += 1
    return action_dict
