from kaggle_environments import make, evaluate


def won_game_percentage(rewards):
    wins = 0
    ties = 0
    loses = 0
    for r in rewards:
        r0 = 0 if r[0] is None else r[0]
        r1 = 0 if r[1] is None else r[1]
        if r0 > r1:
            wins += 1
        elif r1 > r0:
            loses += 1
        else:
            ties += 1
    return f"wins={wins/len(rewards)}, ties={ties/len(rewards)}, loses={loses/len(rewards)}"


def run_single_game():
    env = make("halite", debug=True)
    env.render()
    env.run([None, "random"])


def run_evaluate():
    print(
        won_game_percentage(
            evaluate(
                "halite",
                ["src/agents/random_agent.py", "random"],
                num_episodes=10,
                configuration={"agentExec": "LOCAL"},
            )
        ),
    )
