import random
import re
import subprocess
import sys
import termios
import tty
from typing import TypedDict, cast
from .maze import Maze
from .maze_color import THEMES
from .print_promt import ALGOS, algo_panel, flush
from .parsing import MazeArgs

ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
INSIDE_WIDTH = 51



def _ansi_row(text: str = "", inside_width: int = INSIDE_WIDTH) -> str:
    visible_text = ANSI_RE.sub("", text)
    padding = max(inside_width - len(visible_text), 0)
    return f"║{text}{' ' * padding}║"


def promt_after_maze_print(m: Maze, args: MazeArgs) -> int | None:
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
            row(
                "\033[33m► 1) regenerate\033[0m"
                "        \033[35m║ written by:\033[0m"
            ),
            row("\033[33m► 2) change_color\033[0m      \033[35m║\033[0m"),
            row(
                "\033[33m► 3) change variables\033[0m"
                "  \033[35m║ - alfiorav\033[0m"
            ),
            row(
                "\033[33m► 4) change algorithm\033[0m"
                "  \033[35m║ - kr1\033[0m"
            ),
            row("\033[33m► 5) generate seed\033[0m     \033[35m║\033[0m"),
            row(
                "\033[31m►\033[33m \033[32m6\033[36m)\033[34m "  # noqa: E501
                "\033[35mr\033[31ma\033[33mn\033[32md"  # noqa: E501
                "\033[36mo\033[34mm\033[35m \033[31mc\033[33mo"  # noqa: E501
                "\033[32ml\033[36mo\033[34mr\033[0m"  # noqa: E501
                "      \033[35m║ -\033[0m \033[34mmeow.inc\033[0m"  # noqa: E501
            ),
            row("\033[33m► 7) change speed\033[0m      \033[35m║\033[0m"),
            row("\033[31m► 8) exit\033[0m              \033[35m║\033[0m"),
            row(),
            row(),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select = int(input("\033[36m► select an option\033[0m: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        flush()
        m.print_maze(color=args['COLOR'])
        return promt_after_maze_print(m, args)

    if select not in [1, 2, 3, 4, 5, 6, 7, 8]:
        print("Invalid selection. Please enter 1, 2, 3, 4, 5, 6, 7 or 8")
        flush()
        m.print_maze(color=args['COLOR'])
        return promt_after_maze_print(m, args)
    return select


def tput(*args: str) -> None:
    subprocess.run(["tput", *args], check=True)


# tput_ed_flush is deprecated - use flush() from print_promt instead


def _find_current_theme_name(m: Maze) -> str:
    for name, theme in THEMES.items():
        if theme == m.colors:
            return name
    return "custom"


def color_promt(m: Maze, args: MazeArgs, flag: int = 2) -> None:
    themes = list(THEMES.keys())
    menu_height = len(themes) + 13

    while True:
        if flag == 2:
            flush()
            m.print_maze(color=args['COLOR'])
        elif flag == 1:
            flush()
            m.print_maze(color=args['COLOR'])

        def row(text: str = "") -> str:
            return _ansi_row(text)

        current_theme = args.get('COLOR', _find_current_theme_name(m))
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

        # input con gestione degli errori
        try:
            select_try = read_until_enter("\033[36m► select a option\033[0m: ")
            if _is_cancel_signal(select_try):
                flush()
                m.print_maze(color=args['COLOR'])
                return
            select = int(select_try)
        except ValueError:
            print("Invalid input. Please enter a number.")
            flag = 1  # per ridisegnare la schermata più in basso
            continue  # ricomincia il loop

        if select == 0:
            selected_theme = random.choice(themes)
            args["COLOR"] = selected_theme
            m.colors = THEMES[selected_theme]
            flush()
            m.print_maze(color=args['COLOR'])
            return  # uscita dalla funzione

        if select == len(themes) + 1:
            flush()
            m.print_maze(color=args['COLOR'])
            return  # back al menu principale

        if select < 0 or select > len(themes):
            print(f"Invalid selection. Please enter 0 to {len(themes) + 1}.")
            flag = 1
            continue  # ricomincia il loop

        # Se siamo qui, l'input è valido e corrisponde a un tema
        selected_theme = themes[select - 1]
        args["COLOR"] = selected_theme
        m.colors = THEMES[selected_theme]
        flush()
        m.print_maze(color=args['COLOR'])
        return  # uscita dalla funzione


def get_key() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_until_enter(prompt: str = "> ") -> str:
    print(prompt, end="", flush=True)
    chars: list[str] = []

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
        return -1
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
    value = input("the seed: ").__hash__()
    return value


def _ask_speed(prompt: str, axis_name: str) -> float | None:
    raw = input("the speed: ")
    try:
        value = float(raw)
    except ValueError:
        print("\033[31mInvalid input. Please enter a decimal number.\033[0m")
        return None
    if value <= 0:
        print("\033[31mInvalid input. Speed must be greater than 0.\033[0m")
        return None
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
            "  \033[35m► 7) maze_animation\033[0m"
            f"     {_status(bool(args['MAZE_ANIMATION']))}"
        ),
        _ansi_row(
            "  \033[35m► 8) res_animation\033[0m"
            f"     {_status(bool(args['RES_ANIMATINON']))}"
        ),
        _ansi_row(
            "  \033[35m► 9) random_42\033[0m"
            f"     {_status(bool(args['RANDOM_42']))}"
        ),
        _ansi_row(),
        _ansi_row("  \033[31m► 0) apply + back\033[0m"),
        _ansi_row("  \033[34mRanges: size 1-44, points in bounds\033[0m"),
        _ansi_row("  \033[34mESC applies and closes\033[0m"),
        "╚═══════════════════════════════════════════════════╝",
        "",
    ]
    print("\n".join(box))


def _update_height(m: Maze, args: MazeArgs) -> bool:
    line_count = -1
    while True:
        height = _ask_size("Enter new height (1-44): ", "Height")
        line_count += 1
        if height is None:
            continue
        if height <= 6 or height > 44:
            print("\033[31mInvalid input. Height must be between 7 and 44.\033[0m")
            line_count += 1
            continue
        if args['ENTRY'][0] >= height or args['EXIT'][0] >= height:
            print("\033[31mInvalid input. Entry/exit Y out of bounds.\033[0m")
            line_count += 1
            continue
        args['HEIGHT'] = height
        flush()
        m.print_maze(color=args['COLOR'])
        break
    return True


def _update_width(m: Maze, args: MazeArgs) -> bool:
    line_count = -1
    while True:
        width = _ask_size("Enter new width (1-44): ", "Width")
        line_count += 1
        if width is None:
            continue
        if width < 9 or width > 44:
            print("\033[31mInvalid input. Width must be between 9 and 44.\033[0m")
            line_count += 1
            continue
        if args['ENTRY'][1] >= width or args['EXIT'][1] >= width:
            print("\033[31mInvalid input. Entry/exit X out of bounds.\033[0m")
            line_count += 1
            continue
        args['WIDTH'] = width
        flush()
        m.print_maze(color=args['COLOR'])
        break
    return True


def check_if_inside_42(args: MazeArgs) -> int:
    center_col = args['WIDTH'] // 2
    center_row = args['HEIGHT'] // 2
    start_row = center_row - 4 // 2
    start_col = center_col - 6 // 2
    for i in range(4):
        for j in range(6):
            if (i == 0 or i == 3) and (j == 0 or j == 5):
                continue
            if args['ENTRY'][0] == start_col + j and args['ENTRY'][1] == start_row + i:
                print("\033[31mInvalid input. Entry cannot be inside the initial 42 pattern.\033[0m")
                return 1
            if args['EXIT'][0] == start_col + j and args['EXIT'][1] == start_row + i:
                print("\033[31mInvalid input. Exit cannot be inside the initial 42 pattern.\033[0m")
                return 1
    return 0




def _update_entry(m: Maze, args: MazeArgs) -> bool:
    line_count = -1
    while True:
        point = _ask_point("entry")
        line_count += 1
        if point is None:
            continue

        entry_x, entry_y = point
        in_bounds = 0 <= entry_x < args['WIDTH'] and 0 <= entry_y < args['HEIGHT']
        if not in_bounds:
            print("\033[31mInvalid input. Entry is out of bounds.\033[0m")
            line_count += 1
            continue
        if point == args['EXIT']:
            print(
                "\033[31mInvalid input. "
                "Entry and exit cannot be the same.\033[0m"
            )
            line_count += 1
            continue
        old_entry = args['ENTRY']
        args['ENTRY'] = point
        if check_if_inside_42(args) == 1:
            args['ENTRY'] = old_entry
            line_count += 1
            continue
        else:
            break
    flush()
    m.print_maze(color=args['COLOR'])
    return True


def _update_exit(m: Maze, args: MazeArgs) -> bool:
    line_count = -1
    while True:
        point = _ask_point("exit")
        line_count += 1
        if point is None:
            continue
        exit_x, exit_y = point
        in_bounds = 0 <= exit_x < args['WIDTH'] and 0 <= exit_y < args['HEIGHT']
        if not in_bounds:
            print(
                "\033[31mInvalid input. "
                "Exit coordinates are out of bounds.\033[0m"
            )
            line_count += 1
            continue
        if point == args['ENTRY']:
            print(
                "\033[31mInvalid input. "
                "Exit and entry cannot be the same.\033[0m"
            )
            line_count += 1
            continue
        old_exit = args['EXIT']
        args['EXIT'] = point
        if check_if_inside_42(args) == 1:
            breakpoint()
            args['EXIT'] = old_exit
            line_count += 1
            continue
        else:
            break
    flush()
    m.print_maze(color=args['COLOR'])
    return False


def change_params_after(args: MazeArgs, m: Maze) -> None:
    while True:
        flush()
        m.print_maze(color=args['COLOR'])
        _print_change_params_box(args)

        select_raw = read_until_enter("\033[36m► select an option\033[0m: ")
        if _is_cancel_signal(select_raw):
            flush()
            m.print_maze(color=args['COLOR'])
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
            flush()
            m.print_maze(color=args['COLOR'])
            return

        if select == 1:
            if not _update_height(m, args):
                flush()
                m.print_maze(color=args['COLOR'])
                return

        elif select == 2:
            if not _update_width(m, args):
                flush()
                m.print_maze(color=args['COLOR'])
                return

        elif select == 3:
            if not _update_entry(m, args):
                flush()
                m.print_maze(color=args['COLOR'])
                return

        elif select == 4:
            if not _update_exit(m, args):
                flush()
                m.print_maze(color=args['COLOR'])
                return

        elif select == 5:
            new_seed = _ask_seed("Enter new seed (1-1000000000): ", "Seed")
            if new_seed is None:
                flush()
                m.print_maze(color=args['COLOR'])
                return
            args['SEED'] = new_seed
        elif select == 6:
            args['PERFECT'] = not bool(args['PERFECT'])

        elif select == 7:
            args['MAZE_ANIMATION'] = not bool(
                args['MAZE_ANIMATION']
            )
        elif select == 8:
            args['RES_ANIMATINON'] = not bool(
                args['RES_ANIMATINON']
            )
        elif select == 9:
            if args['ALGORITHM'] in ['back', 'prim']:
                args['RANDOM_42'] = not bool(args['RANDOM_42'])
            else:
                print("\033[31mInvalid selection. Recursive division cannot handle 42.\033[0m")


def after_maze_print(args: MazeArgs, m: Maze) -> None:
    while True:
        select = promt_after_maze_print(m, args)

        if select == 1:
            args['SEED'] = random.randint(0, 10**9)
            random.seed(args['SEED'])
            selection_function(args)
            return

        elif select == 2:
            color_promt(m, args)

        elif select == 3:
            change_params_after(args, m)

        elif select == 4:
            flush()
            m.print_maze(color=args['COLOR'])
            algo_select = algo_panel(args['ALGORITHM'])
            if algo_select is not None:
                args['ALGORITHM'] = ALGOS[algo_select - 1][1]
                selection_function(args)
                return

        elif select == 5:
            if args['SEED'] is not None:
                print(f"Current seed: {args['SEED']}")
            else:
                print("No seed generated yet.")

            new_seed = _ask_seed("Enter new seed (1-1000000000): ", "Seed")
            if new_seed is not None:
                args['SEED'] = new_seed
                random.seed(new_seed)
                selection_function(args)
                return

        elif select == 6:
            flush()
            args["COLOR"] = random.choice(list(THEMES.keys()))
            m.print_maze(color=args['COLOR'])

        elif select == 7:
            flush()
            m.print_maze(color=args['COLOR'])
            print(f"current animation speed:{m.anim_speed}")
            new_speed = _ask_speed("Enter speed (1-0.0000000001): ", "speed")
            if new_speed is None:
                continue
            args['ANIMATION_SPEED'] = new_speed
            selection_function(args)
            return

        elif select == 8:
            flush()
            m.print_maze(color=args['COLOR'])
            print("Goodbye :(")
            exit(1)

def selection_algoritm(m: Maze, args: MazeArgs, cols: int, rows: int) -> None:
    match args['ALGORITHM']:
        case 'back':
            if args['RANDOM_42'] is True:
                m.random_draw_42(cols, rows)
            else:
                m.draw_42(cols, rows)
            m.backtracking(m.grid[0][0], args['MAZE_ANIMATION'], args.get('COLOR', args['COLOR']))
            if not args["PERFECT"]:
                m.break_random_walls(50)
        case 'prim':
            if args['RANDOM_42'] is True:
                m.random_draw_42(cols, rows)
            else:
                m.draw_42(cols, rows)
            m.prim_algoritm(m.grid[0][0], args['MAZE_ANIMATION'], args.get('COLOR', args['COLOR']))
            if not args["PERFECT"]:
                m.break_random_walls(30)
        case 'div':
            m.iterative_division(args['MAZE_ANIMATION'], args.get('COLOR', args['COLOR']))
            if not args["PERFECT"]:
                m.break_random_walls(30)



def selection_function(args: MazeArgs) -> None:
    flush()
    seed_value = args['SEED']
    if seed_value is None:
        seed_value = random.randint(0, 10**9)
        args['SEED'] = seed_value
    random.seed(seed_value)

    cols = args['HEIGHT']
    rows = args['WIDTH']
    start = args['ENTRY']
    end = args['EXIT']
    m = Maze(cols, rows, start, end)
    try:
        m.anim_speed = float(args["ANIMATION_SPEED"])
    except (ValueError, TypeError):
        print("\033[31mInvalid animation speed. Using default value.\033[0m")
        m.anim_speed = 0.001
    start_row, start_col = m.start
    end_row, end_col = m.end
    m.grid[start_row][start_col].start = True
    m.grid[end_row][end_col].end = True
    selection_algoritm(m, args, cols, rows)
    m.bfs(args["RES_ANIMATINON"], args.get('COLOR', args['COLOR']))
    m.print_maze(args.get('COLOR', 'default'))
    m.print_hexa_maze(args["OUTPUT_FILE"])
    after_maze_print(args, m)
