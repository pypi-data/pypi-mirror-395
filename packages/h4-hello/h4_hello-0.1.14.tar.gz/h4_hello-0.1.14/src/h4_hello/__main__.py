import argparse

from . import __version__
from ._core import goodbye, hello


def main() -> None:
    parser = argparse.ArgumentParser(
        description="A simple hello world example",
        prog="h4-hello",
    )
    parser.add_argument(
        "-V",
        "--version",
        action="version",
        version=f"%(prog)s v{__version__}",
    )
    parser.add_argument(
        "-g",
        "--goodbye",
        action="store_true",
        help="Display goodbye message",
    )

    args = parser.parse_args()
    if args.goodbye:
        print(goodbye())
    else:
        print(hello())


if __name__ == "__main__":
    main()
