from random import choice


def first_agent(obs):
    action_dict = {}
    first_ship_id = list(obs.players[obs.player][2].keys())[0]
    ship_action = choice(["NORTH", "SOUTH", "EAST", "WEST", None])

    if ship_action is not None:
        action_dict[first_ship_id] = ship_action

    return action_dict
