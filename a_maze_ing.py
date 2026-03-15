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
        """programmare che colore randomico o scelto rimanga anche dopo la rigenerazione del labirinto, altrimenti è inutile"""
    except (Exception, EOFError, KeyboardInterrupt) as e:
        print(f"\033[31mAn error occurred: {e}\033[0m")
