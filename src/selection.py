



from .maze import Maze
from .print_promt import print_promt, flush


def selection_function(args: list):
    while True:
        print("\033[3J\033[H", end="")
        args = print_promt(args=args)
        """ breakpoint() """
        flush()
        random_42 = True
        cols, rows = args[0], args[1]
        start = args[2]
        end = args[3]
        m = Maze(cols, rows, start, end)
        start_row, start_col = m.start
        end_row, end_col = m.end
        m.grid[start_row][start_col].start = True
        m.grid[end_row][end_col].end = True
        if random_42 is True:
            m.random_draw_42(cols, rows)
        else:
            m.draw_42(cols, rows)
        m.backtracking(m.grid[0][0], True, args[4])
        m.bfs(True)
        m.print_maze()
        m.print_hexa_maze("hexa.txt")
        input("\nPress ENTER to continue...")
        print('\033[3J\033[H')

