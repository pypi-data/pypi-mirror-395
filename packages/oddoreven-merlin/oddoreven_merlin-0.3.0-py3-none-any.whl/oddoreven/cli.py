import argparse
from .core import check


def main():
    parser = argparse.ArgumentParser(
        description="Check whether a number is odd or even."
    )
    parser.add_argument(
        "number",
        type=int,
        help="The integer number you want to check.",
    )

    args = parser.parse_args()
    result = check(args.number)
    print(result)


if __name__ == "__main__":
    main()
