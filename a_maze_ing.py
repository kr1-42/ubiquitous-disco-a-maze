from src.parsing import parse_args
from src.maze import selection_function
from sys import argv

if __name__ == "__main__":
    print("This is a maze game. You can move up, down, left, or right.")
    print("Try to find the exit!")
    if (len(argv) != 1):
        args = parse_args()
    else:
        args = [
            int(input("height")),
            int(input("width")),
            tuple(int(x) for x in input("entry (n,n)").split(',')),
            tuple(int(x) for x in input("exit (n,n)").split(','))
        ]
    selection_function(args[0], args[1], args[2], args[3])
