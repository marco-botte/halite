from kaggle_environments import make


def run_single_game():
    env = make("halite", debug=True)
    env.render()
    env.run(["src/agents/random_agent.py", "random"])
