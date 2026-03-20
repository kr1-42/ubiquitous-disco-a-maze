import random
import re
import subprocess
import sys
import termios
import tty
from typing import TypedDict, cast

from .maze import Maze
from .print_promt import ALGOS, algo_panel, flush
from .maze_color import THEMES


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
INSIDE_WIDTH = 51


class MazeArgs(TypedDict):
    HEIGHT: int
    WIDTH: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool
    ALGORITHM: str
    MAZE_ANIMATION: bool
    RES_ANIMATINON: bool
    RANDOM_42: bool
    SEED: int | None


def _ansi_row(text: str = "", inside_width: int = INSIDE_WIDTH) -> str:
    visible_text = ANSI_RE.sub("", text)
    padding = max(inside_width - len(visible_text), 0)
    return f"║{text}{' ' * padding}║"


def promt_after_maze_print():
    def row(text: str = "") -> str:
        return _ansi_row(text)

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
            row("\033[33m► 5) generate seed\033[0m]    \033[35m║\033[0m"),
            row("\033[31m►\033[33m \033[32m6\033[36m)\033[34m \033[35mr\033[31ma\033[33mn\033[32md\033[36mo\033[34mm\033[35m \033[31mc\033[33mo\033[32ml\033[36mo\033[34mr\033[0m      \033[35m║ -\033[0m \033[34mmeow.inc\033[0m"),
            row("\033[31m► 7) exit\033[0m              \033[35m║\033[0m"),
            row(),
            row(),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select = int(input("\033[36m► select an option\033[0m: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        tput_ed_flush(24)
        promt_after_maze_print()
        return

    if select not in [1, 2, 3, 4, 5, 6, 7]:
        print("Invalid selection. Please enter 1, 2, 3, 4, 5, 6, or 7.")
        tput_ed_flush(24)
        promt_after_maze_print()
        return
    return select


def tput(*args: str) -> None:
    # Emit terminal control codes through `tput` to preserve the maze on screen.
    subprocess.run(["tput", *args], check=True)


def tput_ed_flush(n: int = 19) -> None:
    for _ in range(n):
        tput("cuu1")
        tput("ed")


def _find_current_theme_name(m: Maze) -> str:
    for name, theme in THEMES.items():
        if theme == m.colors:
            return name
    return "custom"


def color_promt(m: Maze, flag: int = 2):
    themes = list(THEMES.keys())
    menu_height = len(themes) + 12

    if flag == 2:
        tput_ed_flush()
    elif flag == 1:
        tput_ed_flush(menu_height)

    def row(text: str = "") -> str:
        return _ansi_row(text)

    current_theme = _find_current_theme_name(m)
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
        tput_ed_flush(menu_height)
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
        if ch in ("\r", "\n"):
            print()
            return "".join(chars)
        if ch == "\x7f":
            if chars:
                chars.pop()
                print("\b \b", end="", flush=True)
            continue
        if ch in ("\x1b", "\x03"):
            return ch

        chars.append(ch)
        print(ch, end="", flush=True)


def _is_cancel_signal(value: str) -> bool:
    return value in ("\x1b", "\x03")


def _read_int_value(prompt: str) -> int | None:
    raw = read_until_enter(prompt)
    if _is_cancel_signal(raw):
        return None
    try:
        return int(raw)
    except ValueError:
        print("\033[31mInvalid input. Please enter a number.\033[0m")
        return -1


def _ask_size(prompt: str, axis_name: str) -> int | None:
    while True:
        value = _read_int_value(prompt)
        if value is None:
            return None
        if value == -1:
            continue
        if 1 <= value <= 44:
            return value
        print(
            f"\033[31mInvalid input. {axis_name} "
            "must be between 1 and 44.\033[0m"
        )


def _ask_seed(prompt: str, axis_name: str) -> int | None:
    value = input("the seed:").__hash__()
    return value


def _ask_point(prefix: str) -> tuple[int, int] | None:
    while True:
        x_value = _read_int_value(f"Enter new {prefix} X: ")
        if x_value is None:
            return None
        if x_value == -1:
            continue

        y_value = _read_int_value(f"Enter new {prefix} Y: ")
        if y_value is None:
            return None
        if y_value == -1:
            continue
        return (x_value, y_value)


def _status(value: bool) -> str:
    if value:
        return "\033[32m[ON]\033[0m"
    return "\033[31m[OFF]\033[0m"


def _print_change_params_box(args: MazeArgs) -> None:
    box = [
        "╔═══════════════════════════════════════════════════╗",
        _ansi_row(),
        _ansi_row("              \033[36m► Change Params\033[0m"),
        _ansi_row("      \033[33mValidate values before regenerate\033[0m"),
        _ansi_row(),
        _ansi_row(
            f"  \033[35m► 1) height\033[0m   \033[32m[{args['HEIGHT']}]\033[0m"
        ),
        _ansi_row(
            f"  \033[35m► 2) width\033[0m    \033[32m[{args['WIDTH']}]\033[0m"
        ),
        _ansi_row(
            f"  \033[35m► 3) entry\033[0m    \033[32m[{args['ENTRY']}]\033[0m"
        ),
        _ansi_row(
            f"  \033[35m► 4) exit\033[0m     \033[32m[{args['EXIT']}]\033[0m"
        ),
        _ansi_row(
            f"  \033[35m► 5) seed\033[0m     \033[32m[{args['SEED']}]\033[0m"
        ),
        _ansi_row(
            f"  \033[35m► 6) perfect\033[0m  {_status(bool(args['PERFECT']))}"
        ),
        _ansi_row(
            f"  \033[35m► 7) maze_animation\033[0m     {_status(bool(args['MAZE_ANIMATION']))}"
        ),
        _ansi_row(
            f"  \033[35m► 8) res_animation\033[0m     {_status(bool(args['RES_ANIMATINON']))}"
        ),
        _ansi_row(
            f"  \033[35m► 9) random_42\033[0m     {_status(bool(args['RANDOM_42']))}"
        ),
        _ansi_row(),
        _ansi_row("  \033[31m► 0) apply + back\033[0m"),
        _ansi_row("  \033[34mRanges: size 1-44, points in bounds\033[0m"),
        _ansi_row("  \033[34mESC applies and closes\033[0m"),
        "╚═══════════════════════════════════════════════════╝",
        "",
    ]
    print("\n".join(box))


def _update_height(args: MazeArgs) -> bool:
    height = _ask_size("Enter new height (1-44): ", "Height")
    if height is None:
        return False
    if args['ENTRY'][1] >= height or args['EXIT'][1] >= height:
        print("\033[31mInvalid input. Entry/exit Y out of bounds.\033[0m")
        return True
    args['HEIGHT'] = height
    return True


def _update_width(args: MazeArgs) -> bool:
    width = _ask_size("Enter new width (1-44): ", "Width")
    if width is None:
        return False
    if args['ENTRY'][0] >= width or args['EXIT'][0] >= width:
        print("\033[31mInvalid input. Entry/exit X out of bounds.\033[0m")
        return True
    args['WIDTH'] = width
    return True


def _update_entry(args: MazeArgs) -> bool:
    point = _ask_point("entry")
    if point is None:
        return False

    entry_x, entry_y = point
    in_bounds = 0 <= entry_x < args['WIDTH'] and 0 <= entry_y < args['HEIGHT']
    if not in_bounds:
        print("\033[31mInvalid input. Entry is out of bounds.\033[0m")
        return True
    if point == args['EXIT']:
        print(
            "\033[31mInvalid input. "
            "Entry and exit cannot be the same.\033[0m"
        )
        return True
    args['ENTRY'] = point
    return True


def _update_exit(args: MazeArgs) -> bool:
    point = _ask_point("exit")
    if point is None:
        return False

    exit_x, exit_y = point
    in_bounds = 0 <= exit_x < args['WIDTH'] and 0 <= exit_y < args['HEIGHT']
    if not in_bounds:
        print(
            "\033[31mInvalid input. "
            "Exit coordinates are out of bounds.\033[0m"
        )
        return True
    if point == args['ENTRY']:
        print(
            "\033[31mInvalid input. "
            "Exit and entry cannot be the same.\033[0m"
        )
        return True
    args['EXIT'] = point
    return True


def change_params_after(args, m) -> None:
    _ = m
    typed_args = cast(MazeArgs, args)

    while True:
        tput_ed_flush(20)
        _print_change_params_box(typed_args)

        select_raw = read_until_enter("\033[36m► select an option\033[0m: ")
        if _is_cancel_signal(select_raw):
            tput_ed_flush(20)
            return

        try:
            select = int(select_raw)
        except ValueError:
            print("\033[31mInvalid input. Please enter a number.\033[0m")
            continue

        if select not in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9]:
            print(
                "\033[31mInvalid selection. "
                "Please enter a number between 0 and 9.\033[0m"
            )
            continue

        if select == 0:
            tput_ed_flush(20)
            return

        if select == 1:
            if not _update_height(typed_args):
                tput_ed_flush(20)
                return

        elif select == 2:
            if not _update_width(typed_args):
                tput_ed_flush(20)
                return

        elif select == 3:
            if not _update_entry(typed_args):
                tput_ed_flush(20)
                return

        elif select == 4:
            if not _update_exit(typed_args):
                tput_ed_flush(20)
                return


        elif select == 5:
            new_seed = _ask_seed("Enter new seed (1-1000000000): ", "Seed")
            if new_seed is None:
                tput_ed_flush(20)
                return
            typed_args['SEED'] = new_seed
        elif select == 6:
            typed_args['PERFECT'] = not bool(typed_args['PERFECT'])

        elif select == 7:
            typed_args['MAZE_ANIMATION'] = not bool(typed_args['MAZE_ANIMATION'])
        elif select == 8:
            typed_args['RES_ANIMATINON'] = not bool(typed_args['RES_ANIMATINON'])
        elif select == 9:
            typed_args['RANDOM_42'] = not bool(typed_args['RANDOM_42'])


def after_maze_print(args: dict, m: Maze, seed: int | None = None) -> None:
    select = promt_after_maze_print()
    if select == 1:
        selection_function(args)
        return
    if select == 2:
        color_promt(m, select)
        after_maze_print(args, m)
        return
    if select == 3:
        change_params_after(args, m)
        after_maze_print(args, m)
        return
    if select == 4:
        tput_ed_flush()
        algo_select = algo_panel(args['ALGORITHM'])
        if algo_select is not None:
            args['ALGORITHM'] = ALGOS[algo_select - 1][1]
            selection_function(args)
            return
        else:
            after_maze_print(args, m)
            return
    if select == 5:
        if seed is not None:
            print(f"Current seed: {seed}")
        else:
            print("No seed generated yet.")
        new_seed = _ask_seed("Enter new seed (1-1000000000): ", "Seed")
        if new_seed is None:
            after_maze_print(args, m)
            return
        random.seed(new_seed)
        selection_function(args)
        return
    if select == 6:
        m.colors = random.choice(list(THEMES.values()))
        flush()
        m.print_maze()
        after_maze_print(args, m)
        return
    if select == 7:
        tput_ed_flush(6)
        print("Goodbye :(")
        exit(1)


def selection_function(args: dict[str, int | str | tuple[int, int]]) -> None:
    flush()
    typed_args = cast(MazeArgs, args)

    if args.get("SEED") is None:
        seed = random.randint(0, 10**9)
        print(f"Generated seed: {seed}")
    random.seed(args.get("SEED") if args.get("SEED") is not None else seed)

    cols = typed_args['HEIGHT']
    rows = typed_args['WIDTH']
    start = typed_args['ENTRY']
    end = typed_args['EXIT']

    m = Maze(cols, rows, start, end)
    start_row, start_col = m.start
    end_row, end_col = m.end
    m.grid[start_row][start_col].start = True
    m.grid[end_row][end_col].end = True
    if typed_args['RANDOM_42'] is True:
        m.random_draw_42(cols, rows)
    else:
        m.draw_42(cols, rows)
    m.backtracking(m.grid[0][0], True, args['PERFECT'])
    m.bfs(True)
    m.print_maze()
    m.print_hexa_maze("hexa.txt")
    after_maze_print(args, m)
