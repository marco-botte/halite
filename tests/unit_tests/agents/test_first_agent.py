from unittest.mock import Mock

import pytest
from src.agents.first_agent import SIZE, Position, first_agent


def test_first_agent():
    obs_mock = Mock(player=0, players={0: [0, {"shipyard": 118}, {"ship": [116, 0]}]})

    action = first_agent(obs_mock)

    assert action == dict() or action["ship"] in ["NORTH", "SOUTH", "EAST", "WEST"]


def test_position_raises_on_invalid_init():
    with pytest.raises(ValueError):
        Position(SIZE ** 2 + 1)


def test_get_adjacent_positions():
    source_pos = Position(50)
    adjacent = source_pos.get_all_adjacent_positions()

    assert adjacent == [Position(35), Position(65), Position(51), Position(49)]


def test_get_adjacent_positions_border_top_right():
    source_pos = Position(SIZE - 1)
    adjacent = source_pos.get_all_adjacent_positions()

    assert adjacent == [
        Position(SIZE ** 2 - 1),
        Position(2 * SIZE - 1),
        Position(0),
        Position(SIZE - 2),
    ]


def test_get_adjacent_positions_border_bottom_left():
    bottom_left_val = SIZE ** 2 - SIZE
    source_pos = Position(bottom_left_val)
    adjacent = source_pos.get_all_adjacent_positions()

    assert adjacent == [
        Position(bottom_left_val - SIZE),
        Position(0),
        Position(bottom_left_val + 1),
        Position(SIZE ** 2 - 1),
    ]
