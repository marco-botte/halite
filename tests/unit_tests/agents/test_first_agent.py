from queue import Queue
from unittest.mock import Mock

from src.agents.first_agent import (
    SIZE,
    Move,
    Player,
    Position,
    Ship,
    Shipyard,
    board_pos_to_position,
    first_agent,
)


def test_board_pos_to_position():
    assert board_pos_to_position(37) == Position(2, 7)


def test_first_agent():
    obs_mock = Mock(
        player=0,
        players={0: [0, {"shipyard": 118}, {"ship": [116, 0]}]},
        halite=list(range(SIZE ** 2)),
    )

    action = first_agent(obs_mock)

    assert action == dict() or action["ship"] in ["NORTH", "SOUTH", "EAST", "WEST"]


def test_get_all_adjacent_positions():
    source_pos = Position(4, 5)
    adjacent = source_pos.get_all_adjacent_positions()

    assert adjacent == [Position(3, 5), Position(5, 5), Position(4, 6), Position(4, 4)]


def test_get_all_adjacent_positions_border_top_right():
    source_pos = Position(0, SIZE - 1)
    adjacent = source_pos.get_all_adjacent_positions()

    assert adjacent == [
        Position(SIZE - 1, SIZE - 1),
        Position(1, SIZE - 1),
        Position(0, 0),
        Position(0, SIZE - 2),
    ]


def test_get_all_adjacent_positions_border_bottom_left():
    source_pos = Position(SIZE - 1, 0)
    adjacent = source_pos.get_all_adjacent_positions()

    assert adjacent == [
        Position(SIZE - 2, 0),
        Position(0, 0),
        Position(SIZE - 1, 1),
        Position(SIZE - 1, SIZE - 1),
    ]


def test_ship_move():
    ship = Ship("GorchFock", Position(2, 4))
    ship.halite = 10

    ship.move(Move.NORTH)

    assert ship.pos == Position(1, 4)
    assert ship.halite == 9


def test_ship_task():
    ship = Ship("GorchFock", Position(2, 4))

    queue = Queue(maxsize=50)
    queue.put(2)
    ship.set_tasks(queue)

    assert ship.task_queue == queue


def test_player_add_shipyard():
    player = Player()
    player.add_shipyard("Hamburg", 13)

    assert player.halite == 3000
    assert player.shipyards == {"Hamburg": Shipyard("Hamburg", 13)}
