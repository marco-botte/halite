import argparse

from src.run import run_evaluate, run_single_game


def main(args):
    if args.cmd == "single":
        run_single_game()

    elif args.cmd == "eval":
        run_evaluate()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Enter run command")
    parser.add_argument("cmd", help="Keyword for run command")
    args = parser.parse_args()

    main(args)
