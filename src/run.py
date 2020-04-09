from kaggle_environments import evaluate, make


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


def run_single_game():
    env = make("halite", debug=True)
    env.render()
    env.run([None, "random"])


def run_evaluate():
    print(
        won_game_percentage(
            evaluate(
                "halite",
                ["src/agents/first_agent.py", "random"],
                num_episodes=10,
                configuration={"agentExec": "LOCAL"},
            )
        ),
    )
