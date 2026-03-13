from src.print_promt import print_promt
from src.parsing import parse_args
from sys import argv

if __name__ == "__main__":
    print("This is a maze game. You can move up, down, left, or right.")
    print("Try to find the exit!")
    if (len(argv) != 1):
        args = parse_args()
    else:
        args = None
    try:
        print_promt(args=args)
    except (Exception, EOFError, KeyboardInterrupt) as e:
        print(f"An error occurred: {e}")
