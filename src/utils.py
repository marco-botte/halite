from enum import Enum

SIZE = 15


class RunCommand(Enum):
    SINGLE = "single"
    EVAL = "eval"


def won_game_percentage(rewards):
    wins = 0
    ties = 0
    losses = 0

    for reward_list in rewards:
        reward0 = 0 if reward_list[0] is None else reward_list[0]
        reward1 = 0 if reward_list[1] is None else reward_list[1]
        if reward0 > reward1:
            wins += 1
        elif reward1 > reward0:
            losses += 1
        else:
            ties += 1
    return f"wins={wins/len(rewards)}, ties={ties/len(rewards)}, losses={losses/len(rewards)}"
