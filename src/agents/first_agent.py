from __future__ import annotations

from typing import List, Tuple

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
    COLLECT = None


class Position:
    def __init__(self, x: int, y: int):
        self.x = x  # pylint: disable=C0103
        self.y = y  # pylint: disable=C0103

    def __str__(self):
        return f"({self.x},{self.y})"

    def __repr__(self):
        return f"({self.x},{self.y})"

    def __eq__(self, other):
        return self.x == other.x and self.y == other.y

    def get_adjacent_position(self, move: Move) -> Position:
        if move == Move.NORTH:
            return Position((self.x - 1) % SIZE, self.y)
        if move == Move.SOUTH:
            return Position((self.x + 1) % SIZE, self.y)
        if move == Move.EAST:
            return Position(self.x, (self.y + 1) % SIZE)
        if move == Move.WEST:
            return Position(self.x, (self.y - 1) % SIZE)
        if move == Move.COLLECT:
            return self
        raise TypeError

    def get_all_adjacent_positions(self) -> List[Position]:
        return list(
            map(self.get_adjacent_position, [move for move in Move if move.value is not None])
        )


def board_pos_to_position(pos) -> Position:
    return Position(pos // SIZE, pos % SIZE)


class Ship:
    def __init__(self, name: str, pos: Position):
        self.pos = pos
        self.name = name
        self.tasks: List[Move] = []
        self.halite = 0

    def move(self, move: Move) -> None:
        self.pos = self.pos.get_adjacent_position(move)
        self.halite = int(self.halite * 0.9)

    def collect(self, board: np.ndarray) -> None:
        self.halite += int(0.25 * board[self.pos.x][self.pos.y])

    def add_task(self, task: Move) -> None:
        self.tasks.append(task)

    def continue_task(
        self, board: List[float]
    ) -> Move:  # for now assume tasks are only of type Move
        if self.tasks:
            task = self.tasks[0]
            self.tasks = self.tasks[1:]
            if task.value is None:
                self.collect(board)
                return Move.COLLECT
            if task in Move:
                self.move(task)
                return task
            raise TypeError
        raise ValueError

    def navigate_to_pos(self, pos: Position) -> None:
        direct_x = self.pos.x - pos.x
        border_x = (
            (self.pos.x + SIZE - pos.x) if self.pos.x < pos.x else (self.pos.x - (pos.x + SIZE))
        )
        direct_y = self.pos.y - pos.y
        border_y = (
            (self.pos.y + SIZE - pos.y) if self.pos.y < pos.y else (self.pos.y - (pos.y + SIZE))
        )

        delta_x = direct_x if abs(direct_x) < abs(border_x) else border_x
        delta_y = direct_y if abs(direct_y) < abs(border_y) else border_y

        if delta_x > 0:
            for _ in range(abs(delta_x)):
                self.tasks.append(Move.NORTH)
        else:
            for _ in range(abs(delta_x)):
                self.tasks.append(Move.SOUTH)

        if delta_y < 0:
            for _ in range(abs(delta_y)):
                self.tasks.append(Move.EAST)
        else:
            for _ in range(abs(delta_y)):
                self.tasks.append(Move.WEST)

    def collect_in_local_cluster(
        self, halite_matrix: List[float], cluster_size: int
    ) -> bool:  # should later be a good collection algorithm.
        for _ in range(cluster_size ** 2):
            move = choice(list(Move))
            task = choice([move, Move.COLLECT])
            self.add_task(task)
        return True

    def __str__(self):
        return f"Ship(name={self.name}, pos={self.pos}, task={self.tasks}, halite={self.halite}"

    def __repr__(self):
        return f"Ship(name={self.name}, pos={self.pos}, task={self.tasks}, halite={self.halite}"

    def __eq__(self, other):
        return self.name == other.name


class Shipyard:
    def __init__(self, name: str, pos: Position):
        self.pos = pos
        self.name = name
        self.occupied = False

    def __str__(self):
        return f"Shipyard(name={self.name}, pos={self.pos}, occupied={self.occupied})"

    def __repr__(self):
        return f"Shipyard(name={self.name}, pos={self.pos}, occupied={self.occupied}"

    def __eq__(self, other):
        return self.pos == other.pos

    def set_occupied(self) -> None:
        self.occupied = True

    def set_unoccupied(self) -> None:
        self.occupied = False


class Player:
    def __init__(self):
        self.step = 0
        self.ships = dict()
        self.halite = 5000
        self.shipyards = dict()

    def add_shipyard(self, name: str, pos: Position) -> None:
        self.shipyards[name] = Shipyard(name, pos)
        self.halite -= 2000

    def add_ship(self, name: str, pos: Position) -> None:
        self.ships[name] = Ship(name, pos)
        self.halite -= 500

    def remove_ship(self, name: str) -> None:
        if self.ships.get(name) is not None:
            del self.ships[name]
        else:
            raise KeyError

    def convert_ship(self, ship_name: str, yard_name: str) -> None:
        if self.ships.get(ship_name) is not None:
            self.add_shipyard(yard_name, self.ships[ship_name].pos)
            self.remove_ship(ship_name)
        else:
            raise KeyError

    def spawn_ship(self, yard_name: str, ship_name: str) -> None:
        if self.shipyards.get(yard_name) is not None:
            shipyard = self.shipyards[yard_name]
            self.add_ship(ship_name, shipyard.pos)
            shipyard.set_occupied()
        else:
            raise KeyError

    def set_occupations(self) -> None:
        occupied_positions = list(map(lambda x: x.pos, self.ships.values()))

        for shipyard in self.shipyards.values():
            if shipyard.pos not in occupied_positions:
                shipyard.occupied = False
            else:
                shipyard.occupied = True

    def all_ship_positions(self) -> List[Tuple[str, Position]]:
        return list(map(lambda x: (x.name, x.pos), self.ships.values()))

    def crash_test(self) -> bool:
        occupied = self.all_ship_positions()
        if len(set(occupied)) < len(occupied):
            return True
        return False


PLAYER = Player()


def find_halite_cluster(halite_matrix: np.ndarray, cluster_size: int) -> Position:
    best_top_left_pos = Position(0, 0)
    best_value = 0
    for x_ind in range(halite_matrix.shape[0] - cluster_size + 1):
        for y_ind in range(halite_matrix.shape[1] - cluster_size + 1):
            submatrix = halite_matrix[
                x_ind : (x_ind + cluster_size), y_ind : (y_ind + cluster_size)
            ]
            submatrix_value = sum(sum(submatrix))  # type: ignore
            if submatrix_value > best_value:
                best_value = submatrix_value
                best_top_left_pos = Position(x_ind, y_ind)

    return Position(
        best_top_left_pos.x + cluster_size // 2, best_top_left_pos.y + cluster_size // 2
    )


def initialize(obs) -> None:
    shipyards = obs["players"][obs["player"]][1]
    for name, board_pos in shipyards.items():
        PLAYER.add_shipyard(name, board_pos_to_position(board_pos))

    ships = obs["players"][obs["player"]][2]
    for name, props in ships.items():
        PLAYER.add_ship(name, board_pos_to_position(props[0]))
    logger.warning("Initialize finished")


def first_agent(obs):
    logger.warning(f"step {obs['step']}, player {obs['players'][0]}")
    action_dict = {}
    owned_halite = obs["players"][0][0]
    board = np.reshape(np.float32(obs["halite"]), (15, 15))
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
    if PLAYER.ships and owned_halite > 4000 and not PLAYER.shipyards:
        converted_ship_name = choice(list(PLAYER.ships))
        shipyard_name = f"{PLAYER.step+1}-{action_counter}"
        new_shipyard_names.add(shipyard_name)
        PLAYER.convert_ship(converted_ship_name, shipyard_name)
        action_dict[converted_ship_name] = "CONVERT"
        owned_halite -= 2000
        action_counter += 1

    # choose action for each ship
    for ship_name, ship in PLAYER.ships.items():
        if ship_name in new_ship_names:
            continue

        if ship.tasks:
            task = ship.continue_task(board)

        elif ship.halite < 500:
            collects_locally = ship.collect_in_local_cluster(halite_matrix=board, cluster_size=5)
            if collects_locally:
                logger.warning("HERE HE COLLECTS\n\n")
                task = ship.continue_task(board)
            else:
                cluster_center = find_halite_cluster(halite_matrix=board, cluster_size=5)
                ship.navigate_to_pos(cluster_center)
                if not ship.tasks:
                    task = Move.COLLECT
                else:
                    task = ship.continue_task(board)

        elif ship.halite > 2000:
            ship.navigate_to_pos(list(PLAYER.shipyards.values())[0].pos)
            task = ship.continue_task(board)

        elif random() < MOVE_PROB:  # move ship
            task = choice(list(Move))
            ship.move(task)
        else:  # collect
            task = Move.COLLECT
            ship.collect(board)

        if task != Move.COLLECT:
            action_dict[ship_name] = task.value

    PLAYER.set_occupations()
    # spawn ship in random shipyard when no ship in shipyard and no ship available
    spawnable_shipyards = list(
        map(
            lambda x: x.name,
            filter(
                lambda x: x.name not in new_shipyard_names and not x.occupied,
                PLAYER.shipyards.values(),
            ),
        )
    )
    if spawnable_shipyards and owned_halite >= 500 and len(PLAYER.ships) == 0:
        spawning_shipyard_name = choice(list(spawnable_shipyards))
        # only spawn when no ship in shipyard
        ship_name = f"{PLAYER.step+1}-{action_counter}"
        new_ship_names.add(ship_name)
        PLAYER.spawn_ship(spawning_shipyard_name, ship_name)
        action_dict[spawning_shipyard_name] = "SPAWN"
        owned_halite -= 500
        action_counter += 1

    logger.warning(f"Actions:\t {action_dict}")  # pylint: disable = W1202
    PLAYER.step += 1
    return action_dict
