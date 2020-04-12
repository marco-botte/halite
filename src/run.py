from kaggle_environments import evaluate, make

from .agents.first_agent import first_agent
from .utils import EXAMPLE_OBS, won_game_percentage


def run_single_game():
    env = make("halite", debug=True)
    env.render()
    env.run(["src/agents/first_agent.py", None])
    # env.run(["random", "random"])


def run_example_obs():
    first_agent(EXAMPLE_OBS)


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
