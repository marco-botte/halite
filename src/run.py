from kaggle_environments import make

# from .utils import won_game_percentage


def run_single_game():
    env = make("halite", debug=True)
    env.render()
    env.run(["src/agents/first_agent.py", None])
    # env.run(["random", "random"])


# def run_evaluate():
#     print(
#         won_game_percentage(
#             evaluate(
#                 "halite",
#                 ["src/agents/first_agent.py", "random"],
#                 num_episodes=10,
#                 configuration={"agentExec": "LOCAL"},
#             )
#         ),
#     )
