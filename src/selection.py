from .maze import Maze
from .print_promt import flush


def promt_after_maze_print():
    inside_width = 51

    def row(text=""):
        return f"║{text.ljust(inside_width)}║"

    try:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            row(),
            row("              \033[36m► after maze\033[0m"),
            row(),
            row("\033[32m► 1) regenerate\033[0m"),
            row("\033[32m► 2) change_color\033[0m"),
            row("\033[32m► 3) change variables\033[0m"),
            row("\033[31m► 4) exit\033[0m"),
            row(),
            row(),
            row(),
            row(),
            row(),
            row(),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select = int(input("\033[36m► select an option\033[0m: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return promt_after_maze_print()
    if select not in [1, 2, 3, 4]:
        print("Invalid selection. Please enter 1, 2, 3, or 4.")
        return promt_after_maze_print()
    return select


def color_promt(m: Maze):
    


def after_maze_print(args: list, m: Maze):
    select = promt_after_maze_print()
    if select == 1:
        return selection_function(args)
    if select == 2:
        color_promt(m)



def selection_function(args: list):
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
    after_maze_print(args, m)

