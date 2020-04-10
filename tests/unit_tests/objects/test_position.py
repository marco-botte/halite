import pytest

from src.utils import SIZE
from src.objects.position import Position


def test_position_raises_on_invalid_init():
    with pytest.raises(ValueError):
        Position(SIZE ** 2 + 1)


def test_get_adjacent_positions():
    source_pos = Position(50)
    adjacent = source_pos.get_adjacent_positions()

    assert adjacent == [Position(35), Position(65), Position(49), Position(51)]


def test_get_adjacent_positions_border_top_right():
    source_pos = Position(SIZE - 1)
    adjacent = source_pos.get_adjacent_positions()

    assert adjacent == [
        Position(SIZE ** 2 - 1),
        Position(2 * SIZE - 1),
        Position(SIZE - 2),
        Position(0),
    ]


def test_get_adjacent_positions_border_bottom_left():
    bottom_left_val = SIZE ** 2 - SIZE
    source_pos = Position(bottom_left_val)
    adjacent = source_pos.get_adjacent_positions()

    assert adjacent == [
        Position(bottom_left_val - SIZE),
        Position(0),
        Position(SIZE ** 2 - 1),
        Position(bottom_left_val + 1),
    ]
