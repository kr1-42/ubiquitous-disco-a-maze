from .maze import Maze
from .print_promt import print_promt, flush
import random


def selection_function(args: list) -> None:
    while True:
        print("\033[3J\033[H", end="")
        args = print_promt(args=args)
        """ breakpoint() """
        flush()
        random_42 = args[6]
        cols, rows = args[0], args[1]
        start = args[2]
        end = args[3]
        seed = args[7]
        start_row: int = 0
        start_col: int = 0
        end_row: int = 0
        end_col: int = 0
        if seed is None:
            seed = random.randint(0, 10**9)
        random.seed(seed)
        m = Maze(cols, rows, start, end)
        if m.start:
            start_row, start_col = m.start
        if m.end:
            end_row, end_col = m.end
        m.grid[start_row][start_col].start = True
        m.grid[end_row][end_col].end = True
        if random_42 is True:
            m.random_draw_42(cols, rows)
        else:
            m.draw_42(cols, rows)
        m.backtracking(m.grid[0][0], args[5], args[4])
        m.bfs(True)
        m.print_maze()
        m.print_hexa_maze("hexa.txt")
        input("\nPress ENTER to continue...")
        print('\033[3J\033[H')
