from asyncio import sleep
import random
import re
import subprocess
import sys
import termios
import tty
from .maze import Maze
from .print_promt import ALGOS, algo_panel, flush
from .maze_color import THEMES


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")


def _ansi_row(text: str = "", inside_width: int = 51) -> str:
    visible_text = ANSI_RE.sub("", text)
    padding = max(inside_width - len(visible_text), 0)
    return f"║{text}{' ' * padding}║"


def promt_after_maze_print():
    inside_width = 51

    def row(text=""):
        return _ansi_row(text, inside_width)

    try:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            row("      ____ _____ ___  ____ _____  ___ "),
            row("     / __ `/ __ `__ \\/ __ `/_  / / _\\"),
            row("    / /_/ / / / / / / /_/ / / /_/  __/"),
            row("    \\__,_/_/ /_/ /_/\\__,_/ /___/\\___/  \033[35m:)\033[0m"),
            row(),
            row("═══════════════════════════════════════════════════"),
            row(),
            row("\033[33m► 1) regenerate\033[0m        \033[35m║ written by:\033[0m"),
            row("\033[33m► 2) change_color\033[0m      \033[35m║\033[0m"),
            row("\033[33m► 3) change variables\033[0m  \033[35m║ - alfiorav\033[0m"),
            row("\033[33m► 4) change algorithm\033[0m  \033[35m║ - kr1\033[0m"),
            row("\033[31m►\033[33m \033[32m5\033[36m)\033[34m \033[35mr\033[31ma\033[33mn\033[32md\033[36mo\033[34mm\033[35m \033[31mc\033[33mo\033[32ml\033[36mo\033[34mr\033[0m      \033[35m║ -\033[0m \033[34mmeow.inc\033[0m"),
            row("\033[31m► 6) exit\033[0m              \033[35m║\033[0m"),
            row(),
            row(),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select = int(input("\033[36m► select an option\033[0m: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        tput_ed_flush(23)
        return promt_after_maze_print()
    if select not in [1, 2, 3, 4, 5, 6]:
        print("Invalid selection. Please enter 1, 2, 3, 4, 5, or 6.")
        tput_ed_flush(23)
        return promt_after_maze_print()
    return select


def tput(*args: str) -> None:
    # Writes escape codes directly to stdout (like running `tput ...` in a shell)
    subprocess.run(["tput", *args], check=True)


def tput_ed_flush(n: int = 22) -> None:
    for _ in range(n):
        tput("cuu1")  # Move cursor up one line
        tput("ed")  # Clear from cursor to end of screen


def color_promt(m: Maze, flag: int = 0):
    inside_width = 51
    themes = list(THEMES.keys())
    menu_height = len(themes) + 12

    if flag == 2:
        tput_ed_flush()
    elif flag == 1:
        tput_ed_flush(menu_height)

    def row(text=""):
        return _ansi_row(text, inside_width)

    def find_current_theme_name() -> str:
        for name, theme in THEMES.items():
            if theme == m.colors:
                return name
        return "custom"

    current_theme = find_current_theme_name()
    try:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            row(),
            row("              \033[36m► Choose Maze Theme\033[0m"),
            row(f"  Current: \033[33m{current_theme}\033[0m"),
            row(),
        ]
        box.append(row("\033[36m► 0) random theme\033[0m"))
        for index, theme_name in enumerate(themes, start=1):
            box.append(row(f"\033[35m► {index:>2}) {theme_name}\033[0m"))
        box.extend([
            row(),
            row(f"\033[31m► {len(themes) + 1:>2}) back\033[0m"),
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


def change_params_after(args, m) -> None:
    inside_width = 51
    tput_ed_flush(22)

    def row(text=""):
        return _ansi_row(text, inside_width)

    def status(value: bool) -> str:
        if value:
            return "\033[32m[ON]\033[0m"
        return "\033[31m[OFF]\033[0m"
    alr_been = 0
    while True:
        flush = 17

        box = [
            "╔═══════════════════════════════════════════════════╗",
            row(),
            row("              \033[36m► Change Params\033[0m"),
            row("      \033[33mValidate values before regenerate\033[0m"),
            row(),
            row(f"  \033[35m► 1) height\033[0m   \033[32m[{args['HEIGHT']}]\033[0m"),
            row(f"  \033[35m► 2) width\033[0m    \033[32m[{args['WIDTH']}]\033[0m"),
            row(f"  \033[35m► 3) entry\033[0m    \033[32m[{args['ENTRY']}]\033[0m"),
            row(f"  \033[35m► 4) exit\033[0m     \033[32m[{args['EXIT']}]\033[0m"),
            row(f"  \033[35m► 5) perfect\033[0m  {status(bool(args['PERFECT']))}"),
            row(),
            row("  \033[31m► 0) apply + back\033[0m"),
            row("  \033[34mRanges: size 1-44, points in bounds\033[0m"),
            row("  \033[34mESC applies and closes\033[0m"),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))

        select_raw = read_until_enter("\033[36m► select an option\033[0m: ")
        if select_raw in ("\x1b", "\x03"):
            tput_ed_flush(flush)
            return after_maze_print(args, m)

        try:
            select = int(select_raw)
        except ValueError:
            print("Invalid input. Please enter a number.")
            flush += 1
            tput_ed_flush(flush)
            continue

        if select not in [0, 1, 2, 3, 4, 5]:
            tput_ed_flush(flush + alr_been)
            print("\033[31mInvalid selection. " +
                  "Please enter a number between 0 and 5.\033[0m")
            alr_been = 1
            continue

        if select == 0:
            tput_ed_flush(flush + alr_been)
            return after_maze_print(args, m)

        if select == 1:
            while True:
                height_raw = read_until_enter("Enter new height (1-44): ")
                flush += 1
                if height_raw in ("\x1b", "\x03"):
                    tput_ed_flush(flush)
                    return after_maze_print(args, m)
                try:
                    height = int(height_raw)
                except ValueError:
                    print("\033[31mInvalid input. " +
                          "Height must be a number.\033[0m")
                    flush += 1
                    continue
                if not 1 <= height <= 44:
                    print("Invalid input. Height must be between 1 and 44.")
                    flush += 1
                    continue
                if args['ENTRY'][1] >= height or args['EXIT'][1] >= height:
                    print("Invalid input. Entry/exit Y out of bounds.")
                    flush += 1
                    continue
                args['HEIGHT'] = height
                tput_ed_flush(flush)
                break

        elif select == 2:
            while True:
                width_raw = read_until_enter("Enter new width (1-44): ")
                flush += 1
                if width_raw in ("\x1b", "\x03"):
                    tput_ed_flush(flush)
                    return after_maze_print(args, m)
                try:
                    width = int(width_raw)
                except ValueError:
                    print("\033[31mInvalid input. Width must be a number.\033[0m")
                    flush += 1
                    continue
                if not 1 <= width <= 44:
                    print("\033[31mInvalid input. Width must be between 1 and 44.\033[0m")
                    flush += 1
                    continue
                if args['ENTRY'][0] >= width or args['EXIT'][0] >= width:
                    print("\033[31mInvalid input. Entry/exit X out of bounds.\033[0m")
                    flush += 1
                    continue
                args['WIDTH'] = width
                tput_ed_flush(flush)
                break

        elif select == 3:
            while True:
                entry_x_raw = read_until_enter("Enter new entry X: ")
                flush += 1
                if entry_x_raw in ("\x1b", "\x03"):
                    tput_ed_flush(flush)
                    return after_maze_print(args, m)
                entry_y_raw = read_until_enter("Enter new entry Y: ")
                flush += 1
                if entry_y_raw in ("\x1b", "\x03"):
                    tput_ed_flush(flush)
                    return after_maze_print(args, m)
                try:
                    entry_x = int(entry_x_raw)
                    entry_y = int(entry_y_raw)
                except ValueError:
                    print("\033[31mInvalid input. Entry coordinates must be numbers.\033[0m")
                    flush += 1
                    continue
                if not (0 <= entry_x < args['WIDTH'] and 0 <= entry_y < args['HEIGHT']):
                    print("\033[31mInvalid input. Entry is out of bounds.\033[0m")
                    flush += 1
                    continue
                if (entry_x, entry_y) == args['EXIT']:
                    print("\033[31mInvalid input. Entry and exit cannot be the same.\033[0m")
                    flush += 1
                    continue
                args['ENTRY'] = (entry_x, entry_y)
                tput_ed_flush(flush)
                break

        elif select == 4:
            while True:
                exit_x_raw = read_until_enter("Enter new exit X: ")
                flush += 1
                if exit_x_raw in ("\x1b", "\x03"):
                    tput_ed_flush(flush)
                    return after_maze_print(args, m)
                exit_y_raw = read_until_enter("Enter new exit Y: ")
                flush += 1
                if exit_y_raw in ("\x1b", "\x03"):
                    tput_ed_flush(flush)
                    return after_maze_print(args, m)
                try:
                    exit_x = int(exit_x_raw)
                    exit_y = int(exit_y_raw)
                except ValueError:
                    print("\033[31mInvalid input. Exit coordinates must be numbers.\033[0m")
                    flush += 1
                    continue
                if not (0 <= exit_x < args['WIDTH'] and 0 <= exit_y < args['HEIGHT']):
                    print("\033[31mInvalid input. Exit coordinates are out of bounds.\033[0m")
                    flush += 1
                    continue
                if (exit_x, exit_y) == args['ENTRY']:
                    print("\033[31mInvalid input. Exit and entry cannot be the same.\033[0m")
                    flush += 1
                    continue
                args['EXIT'] = (exit_x, exit_y)
                tput_ed_flush(flush)
                break

        elif select == 5:
            args['PERFECT'] = not bool(args['PERFECT'])
            tput_ed_flush(flush)


def after_maze_print(args: dict, m: Maze):
    select = promt_after_maze_print()
    if select == 1:
        return selection_function(args)
    if select == 2:
        color_promt(m, select)
        return after_maze_print(args, m)
    if select == 3:
        change_params_after(args, m)
        return after_maze_print(args, m)
    if select == 4:
        tput_ed_flush()
        algo_select = algo_panel(args['ALGORITHM'])
        if algo_select is not None:
            args['ALGORITHM'] = ALGOS[algo_select - 1][1]
            return selection_function(args)
        else:
            return after_maze_print(args, m)
    if select == 5:
        m.colors = random.choice(list(THEMES.values()))
        flush()
        m.print_maze()
        return after_maze_print(args, m)
    if select == 6:
        tput_ed_flush(6)
        print("Goodbye :(")
        exit(1)


def selection_function(args: dict[str, int | str | tuple[int, int]]) -> None:
    flush()
    seed = args['SEED']
    if seed is None:
        seed = random.randint(0, 10**9)
        print(f"Generated seed: {seed}")
    random.seed(seed)
    random_42 = args['RANDOM_42']
    cols, rows = args['HEIGHT'], args['WIDTH']
    start = args['ENTRY']
    end = args['EXIT']
    m = Maze(cols, rows, start, end)
    start_row, start_col = m.start
    end_row, end_col = m.end
    m.grid[start_row][start_col].start = True
    m.grid[end_row][end_col].end = True
    if random_42 is True:
        m.random_draw_42(cols, rows)
    else:
        m.draw_42(cols, rows)
    m.backtracking(m.grid[0][0], args['MAZE_ANIMATION'], args['PERFECT'])
    m.bfs(args['RES_ANIMATINON'])
    m.print_maze()
    m.print_hexa_maze("hexa.txt")
    after_maze_print(args, m)

