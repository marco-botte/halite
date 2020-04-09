from unittest.mock import Mock

from src.agents.random_agent import random_agent


def test_first_agent():
    obs_mock = Mock(player=1, players={1: [0, 0, {"ship": 3}]})

    action = random_agent(obs_mock)

    assert action.get("ship") is not None
    assert action["ship"] in ["NORTH", "SOUTH", "EAST", "WEST", None]
