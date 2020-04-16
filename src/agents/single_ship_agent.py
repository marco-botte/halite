import numpy as np
from enum import Enum
from copy import deepcopy
from itertools import product


class Move(Enum):
    NORTH = "NORTH"
    SOUTH = "SOUTH"
    EAST = "EAST"
    WEST = "WEST"
    COLLECT = "COLLECT"


class Task(Enum):
    COLLECT = "collect"
    EXPLORE = "explore"
    RETURN = "return"


states = {}


def get_next_position(pos, move: Move):
    if move == Move.NORTH:
        return ((pos[0] - 1) % 15, pos[1])
    if move == Move.SOUTH:
        return ((pos[0] + 1) % 15, pos[1])
    if move == Move.EAST:
        return (pos[0], (pos[1] + 1) % 15)
    if move == Move.WEST:
        return (pos[0], (pos[1] - 1) % 15)
    if move == Move.COLLECT:
        return (pos[0], pos[1])


def get_all_next_positions(pos):
    return list(map(lambda x: get_next_position(pos, x), list(Move)))


def get_dist(pos1, pos2):
    return get_grid_dist(position_to_grid_pos(pos1), position_to_grid_pos(pos2))


def get_grid_dist(pos1, pos2):
    return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])


def projected_collect_halite(curr_pos, collect_pos, dropoff_pos, board, halite, collect_turns):

    halite_value_at_arrival = int(
        1.02 ** (get_grid_dist(curr_pos, collect_pos)) * board[collect_pos[0]][collect_pos[1]]
    )

    collect_gain = int(
        sum([0.25 * halite_value_at_arrival * 0.75 ** turn for turn in range(1, collect_turns + 1)])
    )
    projected_halite = int(
        (0.9 ** (get_grid_dist(curr_pos, collect_pos)) * halite + collect_gain)
        * 0.9 ** (get_grid_dist(collect_pos, dropoff_pos))
    )
    return projected_halite


def projected_halite(curr_pos, moves, dropoff_pos, board, halite):
    board = deepcopy(board)
    for index, move in enumerate(moves):
        if move != Move.COLLECT:
            halite = int(halite * 0.9)
            curr_pos = get_next_position(curr_pos, move)
        else:
            collect_value = int(0.25 * (board[curr_pos[0]][curr_pos[1]] * 1.02 ** index))
            halite += collect_value
            board[curr_pos[0]][curr_pos[1]] -= collect_value

    dropoff_dist = get_grid_dist(curr_pos, dropoff_pos)
    return int((0.9 ** dropoff_dist * halite) / (1.05 ** len(moves)))


def get_best_move(pos, dropoff_pos, halite, board):
    best_value = 0
    best_moves = []

    for move1, move2 in product(list(Move), repeat=2):
        moves = [move1, move2]
        val = projected_halite(pos, moves, dropoff_pos, board, halite)

        if val > best_value:
            best_value = val
            best_moves = moves

    if not best_moves:
        return [Move.NORTH]

    if projected_halite(pos, [], dropoff_pos, board, halite) > best_value:
        best_moves = [grid_navigate_to(pos, dropoff_pos)]

    return best_moves


def grid_navigate_to(from_pos, to_pos):
    return navigate_to(from_pos[0] * 15 + from_pos[1], to_pos[0] * 15 + to_pos[1])


def navigate_to(fromPos, toPos):
    fromY, fromX = divmod(fromPos, 15)
    toY, toX = divmod(toPos, 15)

    if fromY < toY:
        return Move.SOUTH
    if fromY > toY:
        return Move.NORTH
    if fromX < toX:
        return Move.EAST
    if fromX > toX:
        return Move.WEST
    # => already there
    return Move.COLLECT


def evaluate_cluster(cluster_matrix, cluster_center, curr_pos):
    travel_dist = 2 * get_grid_dist(cluster_center, curr_pos)
    evaluation = sum(sum(cluster_matrix)) * 0.9 ** travel_dist  # type: ignore
    return evaluation


def find_halite_cluster(halite_matrix: np.ndarray, cluster_size: int, ship_pos: int):
    grid_pos = position_to_grid_pos(ship_pos)
    best_center_pos = (7, 7)
    best_value = 0

    for x_ind in range(halite_matrix.shape[0] - cluster_size + 1):
        for y_ind in range(halite_matrix.shape[1] - cluster_size + 1):
            submatrix = halite_matrix[
                x_ind : (x_ind + cluster_size), y_ind : (y_ind + cluster_size)
            ]
            curr_center_pos = (x_ind + cluster_size // 2, y_ind + cluster_size // 2)
            submatrix_value = evaluate_cluster(submatrix, curr_center_pos, grid_pos)
            if submatrix_value > best_value:
                best_value = submatrix_value
                best_center_pos = curr_center_pos

    return grid_pos_to_position(best_center_pos)


def grid_pos_to_position(pos):
    return pos[0] * 15 + pos[1]


def position_to_grid_pos(pos):
    return (pos // 15, pos % 15)


def agent(obs):
    action = {}
    player_halite, shipyards, ships = obs.players[obs.player]
    board = np.reshape(np.float32(obs["halite"]), (15, 15))
    # print(player_halite, ships)

    for uid, shipyard in shipyards.items():
        if len(ships) == 0:
            action[uid] = "SPAWN"

    if shipyards:
        shipyard_pos = list(shipyards.values())[0]

    for uid, ship in ships.items():
        if len(shipyards) == 0:
            action[uid] = "CONVERT"
            continue

        # Add new ships to states
        if uid not in states:
            states[uid] = [Task.EXPLORE, find_halite_cluster(board, 3, shipyard_pos)]

        pos, halite = ship
        grid_pos = position_to_grid_pos(pos)

        if get_dist(ship[0], shipyard_pos) > 396 - obs["step"]:
            states[uid] = [Task.RETURN, None]

        if states[uid][0] == Task.COLLECT:
            if states[uid][1]:
                # print("continue!")
                next_move = states[uid][1][0]
                states[uid][1] = states[uid][1][1:]
                if next_move != Move.COLLECT:
                    action[uid] = next_move.value
            else:
                task_list = get_best_move(
                    grid_pos, position_to_grid_pos(shipyard_pos), ship[1], board
                )
                states[uid] = [Task.COLLECT, task_list[1:]]
                if task_list[0] != Move.COLLECT:
                    action[uid] = task_list[0].value
                if ship[0] == shipyard_pos:
                    if ship[1] > 0:
                        # print("DROP!")
                        continue
                    else:
                        # print("explore!")
                        states[uid] = [
                            Task.EXPLORE,
                            find_halite_cluster(board, 3, shipyard_pos),
                        ]

        if states[uid][0] == Task.EXPLORE:
            if get_dist(ship[0], states[uid][1]) > 0:
                next_move = navigate_to(ship[0], states[uid][1])
                action[uid] = next_move.value
            else:
                # print("collect!")
                states[uid] = [Task.COLLECT, []]

        if states[uid][0] == Task.RETURN:
            if get_dist(ship[0], shipyard_pos) > 0:
                next_move = navigate_to(ship[0], shipyard_pos)
                action[uid] = next_move.value
            else:
                continue

    return action
