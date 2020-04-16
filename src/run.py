from kaggle_environments import evaluate, make

from .agents.first_agent import first_agent
from .utils import EXAMPLE_OBS, won_game_percentage


def run_single():
    env = make("halite", debug=True)
    env.render()
    env.run(["src/agents/single_ship_agent.py", None])


def run_test():
    env = make("halite", debug=True)
    for _ in range(10):
        env.run(["src/agents/single_ship_agent.py", None])


def run_example_obs():
    first_agent(EXAMPLE_OBS)


def run_evaluate():
    print(
        won_game_percentage(
            evaluate(
                "halite",
                ["src/agents/single_ship_agent.py", "src/agents/single_ship_agent.py"],
                num_episodes=10,
                configuration={"agentExec": "LOCAL"},
            )
        ),
    )
