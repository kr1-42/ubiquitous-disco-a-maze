from asyncio import sleep
import random
import subprocess
import sys
import termios
import tty
from .maze import Maze
from .print_promt import flush
from .maze_color import THEMES


def promt_after_maze_print():
    inside_width = 51

    def row(text=""):
        return f"║{text.ljust(inside_width)}║"

    try:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            row(),
            row("      ____ _____ ___  ____ _____  ___ "),
            row("     / __ `/ __ `__ \\/ __ `/_  / / _\\"),
            row("    / /_/ / / / / / / /_/ / / /_/  __/"),
            row("    \\__,_/_/ /_/ /_/\\__,_/ /___/\\___/  :)"),
            row(),
            row("\033[32m► 1) regenerate\033[0m        ║ written by"),
            row("\033[32m► 2) change_color\033[0m      ║ - alfiorav"),
            row("\033[32m► 3) change variables\033[0m  ║ - kr1"),
            row("\033[31m► 4) exit\033[0m              ║"),
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
        tput_ed_flush(18)
        return promt_after_maze_print()
    return select



def tput(*args: str) -> None:
    # Writes escape codes directly to stdout (like running `tput ...` in a shell)
    subprocess.run(["tput", *args], check=True)


def tput_ed_flush(n: int = 17) -> None:
    for _ in range(n):
        tput("cuu1")  # Move cursor up one line
        tput("ed")  # Clear from cursor to end of screen


def color_promt(m: Maze, flag: int = 0):
    inside_width = 51
    if flag == 2:
        tput_ed_flush()
    elif flag == 1:
        tput_ed_flush(27)
    def row(text=""):
        return f"║{text.ljust(inside_width)}║"

    themes = list(THEMES.keys())
    try:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            row(),
            row("              \033[36m► choose color\033[0m"),
            row(),
        ]
        box.append(row("\033[36m► 0) random\033[0m"))
        for index, theme_name in enumerate(themes, start=1):
            box.append(row(f"\033[35m► {index}) {theme_name}\033[0m"))
        box.extend([
            row(),
            row(f"\033[31m► {len(themes) + 1}) back\033[0m"),
            row(),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ])
        print("\n".join(box))
        select = int(input("\033[36m► select an option\033[0m: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return color_promt(m, 1)

    if select == 0:
        selected_theme = random.choice(list(THEMES.keys()))
        m.colors = THEMES[selected_theme]
        flush()
        m.print_maze()
        return
    if select == len(themes) + 1:
        return
    if select < 1 or select > len(themes):
        print(f"Invalid selection. Please enter 0 to {len(themes) + 1}.")
        return color_promt(m, 1)

    selected_theme = themes[select - 1]
    m.colors = THEMES[selected_theme]
    flush()
    m.print_maze()


def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)



def read_until_enter(prompt="> "):
    print(prompt, end="", flush=True)
    chars = []

    while True:
        ch = get_key()
        if ch in ("\r", "\n"):          # Enter pressed
            print()                     # move to next line
            return "".join(chars)
        if ch == "\x7f":                # Backspace on Linux terminals
            if chars:
                chars.pop()
                print("\b \b", end="", flush=True)
            continue
        if ch == "\x1b" or ch == "\x03":                # ESC or Ctrl+C pressed
            return ch

        chars.append(ch)                # normal char
        print(ch, end="", flush=True)   # echo

def change_params_after(args) -> list:
        tput_ed_flush()
        print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
        print("\033[36m║\033[35m  Enter Parameters                         \033[36m║\033[0m")
        print("\033[36m║\033[35m  ESC to exit dialog                       \033[36m║\033[0m")
        print("\033[36m╚════════════════════════════════════════════════╝\033[0m\n")
        flush = 4
        try:
            while True:
                height = read_until_enter("\033[36m► Height: \033[0m")
                flush += 1
                if height == "\x1b" or height == "\x03":
                    tput_ed_flush(flush)
                    return args
                try:
                    height = int(height)
                except ValueError:
                    print("\n\033[31m✗ Invalid input. Height must be a number.\033[0m\n")
                    flush += 3
                    continue
                if height > 0 and height < 45:
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Height must be between 1 and 44.\033[0m\n")
                    flush += 3
            while True:
                width = read_until_enter("\033[36m► Width: \033[0m")
                flush += 1
                if width == "\x1b" or width == "\x03":
                    tput_ed_flush(flush)
                    return args
                try:
                    width = int(width)
                except ValueError:
                    print("\n\033[31m✗ Invalid input. Width must be a number.\033[0m\n")
                    flush += 3
                    continue
                if width > 0 and width < 45:
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Width must be between 1 and 44.\033[0m\n")
                    flush += 3
            while True:
                entry_x = read_until_enter("\033[36m► Entry X: \033[0m")
                flush += 1
                if entry_x == "\x1b" or entry_x == "\x03":
                    tput_ed_flush(flush)
                    return args
                try:
                    entry_x = int(entry_x)
                except ValueError:
                    print("\n\033[31m✗ Invalid input. Entry X must be a number.\033[0m\n")
                    flush += 3
                    continue
                entry_y = read_until_enter("\033[36m► Entry Y: \033[0m")
                flush += 1
                if entry_y == "\x1b" or entry_y == "\x03":
                    tput_ed_flush(flush)
                    return args
                try:
                    entry_y = int(entry_y)
                except ValueError:
                    print("\n\033[31m✗ Invalid input. Entry Y must be a number.\033[0m\n")
                    flush += 3
                    continue
                if 0 <= entry_x < width and 0 <= entry_y < height:
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Entry coordinates are out of bounds.\033[0m\n")
                    flush += 3
            while True:
                exit_x = read_until_enter("\033[36m► Exit X: \033[0m")
                flush += 1
                if exit_x == "\x1b" or exit_x == "\x03":
                    tput_ed_flush(flush)
                    return args
                try:
                    exit_x = int(exit_x)
                except ValueError:
                    print("\n\033[31m✗ Invalid input. Exit X must be a number.\033[0m\n")
                    flush += 3
                    continue
                if exit_x < 0 or exit_x >= width or exit_x == entry_x:
                    print("\n\033[31m✗ Invalid input. Exit X coordinate is out of bounds or same as entry.\033[0m\n")
                    flush += 3
                if 0 <= exit_x < width and exit_x != entry_x:
                    break
            while True:
                exit_y = read_until_enter("\033[36m► Exit Y: \033[0m")
                flush += 1
                if exit_y == "\x1b" or exit_y == "\x03":
                    tput_ed_flush(flush)
                    return args
                try:
                    exit_y = int(exit_y)
                except ValueError:
                    print("\n\033[31m✗ Invalid input. Exit Y must be a number.\033[0m\n")
                    flush += 3
                    continue
                if 0 <= exit_y < height and exit_y != entry_y:
                    break
                elif exit_y < 0 or exit_y >= height:
                    print("\n\033[31m✗ Invalid input. Exit Y coordinate is out of bounds.\033[0m\n")
                    flush += 3
                    continue

            while True:
                perfect_input = read_until_enter("\033[36m► Perfect maze (y/n): \033[0m")
                flush += 1
                if perfect_input == "\x1b" or perfect_input == "\x03":
                    tput_ed_flush(flush)
                    return args
                perfect_input = perfect_input.strip().lower()
                if perfect_input in ['y', 'yes']:
                    perfect = True
                    break
                elif perfect_input in ['n', 'no']:
                    perfect = False
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Please enter y/yes or n/no.\033[0m\n")
                    flush += 3
            return selection_function([height, width, (entry_x, entry_y), (exit_x, exit_y), perfect, None, 'dfs'])
        except (ValueError, KeyboardInterrupt, EOFError):
            print("\n\033[31m✗ Invalid input. Please enter numbers."
                  "\033[0m\n")
            return selection_function(args)


def after_maze_print(args: list, m: Maze):
    select = promt_after_maze_print()
    if select == 1:
        return selection_function(args)
    if select == 2:
        color_promt(m, select)
        return after_maze_print(args, m)
    if select == 3:
        change_params_after(args)
        return after_maze_print(args, m)
    if select == 4:
        tput_ed_flush(6)
        print("Goodbye :(")
        exit(1)


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

