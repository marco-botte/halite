from kaggle_environments import evaluate, make

from .utils import won_game_percentage


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
