from typing import cast

from src.print_promt import MazeArgs, print_promt
from src.parsing import parse_args
from sys import argv

if __name__ == "__main__":
    if (len(argv) != 1):
        args = parse_args()
    else:
        args = cast(MazeArgs, None)
    try:
        print_promt(args=args)
    except (EOFError, KeyboardInterrupt) as e:
        print(f"\n\033[31mAn error occurred: {e}\033[0m")
