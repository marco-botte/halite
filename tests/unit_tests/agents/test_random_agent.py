from unittest.mock import Mock

from src.agents.random_agent import random_agent


def test_random_agent():
    obs_mock = Mock(player=0, players={0: [0, 0, {"ship": 3}], 1: [0, 0, {"ship": 3}]})

    action = random_agent(obs_mock)

    assert action == dict() or action["ship"] in ["NORTH", "SOUTH", "EAST", "WEST"]
