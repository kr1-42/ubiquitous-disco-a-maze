from src.parsing import parse_args
from src.selection import selection_function
from sys import argv

if __name__ == "__main__":
    print("This is a maze game. You can move up, down, left, or right.")
    print("Try to find the exit!")
    if (len(argv) != 1):
        args = parse_args()
    else:
        args = None

    selection_function(args)
