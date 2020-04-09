import logging
from random import choice

logger = logging.getLogger()  # pylint: disable = C0103


def first_agent(obs):
    logger.warning(obs.players[0])

    action_dict = {}

    shipyard_id_list = list(obs.players[obs.player][1].keys())
    ship_id_list = list(obs.players[obs.player][2].keys())

    if obs.players[obs.player][0] > 4000 and ship_id_list:
        action_dict[ship_id_list[0]] = "CONVERT"

    elif obs.players[obs.player][0] >= 1000 and obs.step % 4 == 1 and shipyard_id_list:
        action_dict[shipyard_id_list[0]] = "SPAWN"

    else:
        ship_action = choice(["NORTH", "SOUTH", "EAST", "WEST", None])
        if ship_action is not None:
            action_dict[ship_id_list[0]] = ship_action
    logger.warning(f"Action:\t {action_dict}")  # pylint: disable = W1202
    return action_dict
