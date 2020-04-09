from kaggle_environments import make


def main():
    env = make("halite", debug=True)
    env.render()
    env.run(["src/agents/random_agent.py", "random"])


if __name__ == "__main__":
    main()
