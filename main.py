import argparse

from src.run import run_evaluate, run_example_obs, run_single_game
from src.utils import RunCommand


def main(args):
    if args.cmd not in list(map(lambda x: x.value, RunCommand)):
        raise KeyError

    if args.cmd == "single":
        run_single_game()

    if args.cmd == "eval":
        run_evaluate()

    if args.cmd == "example":
        run_example_obs()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter run command")
    parser.add_argument("cmd", help="Keyword for run command")
    args = parser.parse_args()

    main(args)
