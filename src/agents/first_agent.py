import logging
from enum import Enum
from random import choice, random

logger = logging.getLogger()  # pylint: disable = C0103

SIZE = 15
MOVE_PROB = 0.66


class Move(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"


class Task(Enum):
    COLLECT = "collect"
    DROPOFF = "dropoff"
    CONVERT = "convert"
    ATTACK = "attack"


MOVE_TO_DELTA = {Move.NORTH: -SIZE, Move.SOUTH: SIZE, Move.EAST: 1, Move.WEST: -1}


class Position:
    def __init__(self, pos):
        if pos not in range(SIZE ** 2):
            raise ValueError
        self.value = pos

    def __str__(self):
        return f"Position {self.value}"

    def __repr__(self):
        return f"Position {self.value}"

    def __eq__(self, other):
        return self.value == other.value

    def get_adjacent_position(self, move):
        if move == Move.NORTH or move == Move.SOUTH:
            return Position((self.value + MOVE_TO_DELTA[move]) % (SIZE ** 2))
        elif move == Move.EAST:
            target = self.value + MOVE_TO_DELTA[move]
            if target % SIZE == 0:
                return Position(target - SIZE)
            else:
                return Position(target)
        elif move == Move.WEST:
            target = self.value + MOVE_TO_DELTA[move]
            if target % SIZE == (SIZE - 1):
                return Position(target + SIZE)
            else:
                return Position(target)

    def get_all_adjacent_positions(self):
        return list(map(lambda x: self.get_adjacent_position(x), Move))


class Ship:
    def __init__(self, name, props):
        self.pos = Position(props[0])
        self.name = name
        self.task = Task.COLLECT
        self.halite = props[1]

    def move(self, move):
        self.pos = self.pos.get_adjacent_position(move)
        self.halite *= 0.9

    def set_task(self, task):
        if task not in Task:
            raise ValueError
        self.task = task

    def __str__(self):
        return (
            f"Ship: {self.name},\tpos: {self.pos},\ttask: {self.task.value},\thalite: {self.halite}"
        )

    def __repr__(self):
        return (
            f"Ship: {self.name},\tpos: {self.pos},\ttask: {self.task.value},\thalite: {self.halite}"
        )


class Shipyard:
    def __init__(self, name, pos):
        self.pos = Position(pos)
        self.name = name
        self.occupied = False

    def __str__(self):
        return f"Shipyard: {self.name},\tpos: {self.pos},\tis {'not ' if self.occupied ==False else ''}occupied"

    def __repr__(self):
        return f"Shipyard: {self.name},\tpos: {self.pos},\tis {'not ' if self.occupied ==False else ''}occupied"

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
        self.halite -= 2000

    def add_ship(self, name, props):
        self.ships[name] = Ship(name, props)
        self.halite -= 500

    def remove_ship(self, name):
        if self.ships.get(name) is not None:
            del self.ships[name]
        else:
            raise KeyError

    def convert_ship(self, ship_name, yard_name):
        if self.ships.get(ship_name) is not None:
            pos = self.ships[ship_name].pos.value
            self.remove_ship(ship_name)
            self.add_shipyard(yard_name, pos)
        else:
            raise KeyError

    def spawn_ship(self, yard_name, ship_name):
        if self.shipyards.get(yard_name) is not None:
            shipyard = self.shipyards[yard_name]
            self.add_ship(ship_name, [shipyard.pos.value, 0])
            shipyard.set_occupied()
        else:
            raise KeyError

    def all_ship_positions(self):
        return list(map(lambda x: (x.name, x.pos.value), self.ships.values()))

    def crash_test(self):
        occupied = PLAYER.all_ship_positions()
        if len(set(occupied)) < len(occupied):
            return True
        return False


PLAYER = Player()


def initialize(obs):
    shipyards = obs.players[obs.player][1]
    for name, pos in shipyards.items():
        PLAYER.add_shipyard(name, pos)

    ships = obs.players[obs.player][2]
    for name, props in ships.items():
        PLAYER.add_ship(name, props)
    logger.warning("Initialize finished")


def first_agent(obs):
    logger.warning(f"step {obs.step}, player {obs.players[0]}")
    action_dict = {}
    owned_halite = obs.players[obs.player][0]
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

        # Update Halite for ships in player!

    logger.warning(f"Actions:\t {action_dict}")  # pylint: disable = W1202
    PLAYER.step += 1
    return action_dict
