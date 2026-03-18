import os
import re
import sys
import termios
import tty


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")

ALGOS = [
    ("Depth-First Search (DFS)", "dfs"),
    ("Prim's Algorithm",         "prim"),
    ("Kruskal's Algorithm",      "kruskal"),
]


def _visible_len(text: str) -> int:
    return len(ANSI_RE.sub("", text))


def _ansi_pad(text: str, width: int) -> str:
    return f"{text}{' ' * max(width - _visible_len(text), 0)}"


def _side_row(
    left: str = "",
    right: str = "",
    left_width: int = 31,
    right_width: int = 55,
) -> str:
    return f"║{_ansi_pad(left, left_width)}║{_ansi_pad(right, right_width)}║"


def _box_row(text: str = "", width: int = 51) -> str:
    return f"║{_ansi_pad(text, width)}║"


def _format_param_value(value) -> str:
    if isinstance(value, bool):
        color = "32" if value else "31"
        label = "ON" if value else "OFF"
        return f"\033[{color}m[{label}]\033[0m"
    return f"\033[36m[{value}]\033[0m"


def flush() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def panel() -> int:
    try:
        box = [
            "╔═══════════════════════════════════════════════════════════════════════════════════════╗",
            "║       ___       ___       ___       ___       ___       ___       ___       ___       ║",
            "║      /\\  \\     /\\__\\     /\\  \\     /\\  \\     /\\  \\     /\\  \\     /\\__\\     /\\  \\      ║",
            "║     /::\\  \\   /::L_L_   /::\\  \\   _\\:\\  \\   /::\\  \\   _\\:\\  \\   /:| _|_   /::\\  \\     ║",
            "║    /::\\:\\__\\ /:/L:\\__\\ /::\\:\\__\\ /::::\\__\\ /::\\:\\__\\ /\\/::\\__\\ /::|/\\__\\ /:/\\:\\__\\    ║",
            "║    \\/\\::/  / \\/_/:/  / \\/\\::/  / \\::;;/__/ \\:\\:\\/  / \\::/\\/__/ \\/|::/  / \\:\\:\\/__/    ║",
            "║      /:/  /    /:/  /    /:/  /   \\:\\__\\    \\:\\/  /   \\:\\__\\     |:/  /   \\::/  /     ║",
            "║      \\/__/     \\/__/     \\/__/     \\/__/     \\/__/     \\/__/     \\/__/     \\/__/      ║",
            "╠═══════════════════════════════════════════════════════════════════════════════════════╣",
            _side_row(),
            _side_row(),
            _side_row("\033[35m► 1) Parameters\033[0m", "\033[35mwritten by:\033[0m"),
            _side_row("\033[35m► 2) Algorithm\033[0m", "\033[35m\033[0m"),
            _side_row("\033[35m► 3) run program\033[0m", "\033[35m- alfiorav\033[0m"),
            _side_row("\033[31m► 4) exit\033[0m", "\033[35m- kr1\033[0m"),
            _side_row("", "\033[35m-\033[0m \033[34mmeow.inc\033[0m"),
            _side_row(),
            _side_row(),
            _side_row(),
            _side_row(),
            "╚═══════════════════════════════════════════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select = int(input("\033[36m►Please select an option: \033[0m"))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return panel()
    if select not in [1, 2, 3, 4]:
        print("Invalid selection. Please enter 1, 2, 3, or 4.")
        return panel()
    return select


def params_panel(args: dict[str, int | str | tuple[int, int]]) -> dict[str, int | str | tuple[int, int]]:
    while True:
        flush()
        height_value = _format_param_value(args['HEIGHT'])
        width_value = _format_param_value(args['WIDTH'])
        entry_value = _format_param_value(args['ENTRY'])
        exit_value = _format_param_value(args['EXIT'])
        perfect_value = _format_param_value(args['PERFECT'])

        box = [
            "╔═══════════════════════════════════════════════════╗",
            _box_row(),
            _box_row("              \033[36m► Change Params\033[0m"),
            _box_row("      \033[33mValidate values before generate\033[0m"),
            _box_row(),
            _box_row(f"  \033[35m► 1) height\033[0m   {height_value}"),
            _box_row(f"  \033[35m► 2) width\033[0m    {width_value}"),
            _box_row(f"  \033[35m► 3) entry\033[0m    {entry_value}"),
            _box_row(f"  \033[35m► 4) exit\033[0m     {exit_value}"),
            _box_row(f"  \033[35m► 5) perfect\033[0m  {perfect_value}"),
            _box_row(),
            _box_row("  \033[31m► 0) back\033[0m"),
            _box_row(),
            _box_row("  \033[34mRanges: size 1-44, points must be in bounds\033[0m"),
            _box_row("  \033[34mESC closes the panel too\033[0m"),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select_raw = read_until_enter("\033[36m► select an option\033[0m: ")
        if select_raw in ("\x1b", "\x03"):
            flush()
            return args

        try:
            select = int(select_raw)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if select not in [0, 1, 2, 3, 4, 5]:
            print("Invalid selection. Please enter a number between 0 and 5.")
            continue

        if select == 0:
            flush()
            return args

        if select == 1:
            while True:
                height_raw = read_until_enter("Enter new height (1-44): ")
                if height_raw in ("\x1b", "\x03"):
                    flush()
                    return args
                try:
                    height = int(height_raw)
                except ValueError:
                    print("Invalid input. Height must be a number.")
                    continue
                if not 1 <= height <= 44:
                    print("Invalid input. Height must be between 1 and 44.")
                    continue
                if args['ENTRY'][1] >= height or args['EXIT'][1] >= height:
                    print("Invalid input. Entry/exit Y out of bounds.")
                    continue
                args['HEIGHT'] = height
                break

        elif select == 2:
            while True:
                width_raw = read_until_enter("Enter new width (1-44): ")
                if width_raw in ("\x1b", "\x03"):
                    flush()
                    return args
                try:
                    width = int(width_raw)
                except ValueError:
                    print("Invalid input. Width must be a number.")
                    continue
                if not 1 <= width <= 44:
                    print("Invalid input. Width must be between 1 and 44.")
                    continue
                if args['ENTRY'][0] >= width or args['EXIT'][0] >= width:
                    print("Invalid input. Entry/exit X out of bounds.")
                    continue
                args['WIDTH'] = width
                break

        elif select == 3:
            while True:
                entry_x_raw = read_until_enter("Enter new entry X: ")
                if entry_x_raw in ("\x1b", "\x03"):
                    flush()
                    return args
                entry_y_raw = read_until_enter("Enter new entry Y: ")
                if entry_y_raw in ("\x1b", "\x03"):
                    flush()
                    return args
                try:
                    entry_x = int(entry_x_raw)
                    entry_y = int(entry_y_raw)
                except ValueError:
                    print("Invalid input. Entry coordinates must be numbers.")
                    continue
                if not (0 <= entry_x < args['WIDTH']
                        and 0 <= entry_y < args['HEIGHT']):
                    print("Invalid input. Entry is out of bounds.")
                    continue
                if (entry_x, entry_y) == args['EXIT']:
                    print("Invalid input. Entry and exit cannot be the same.")
                    continue
                args['ENTRY'] = (entry_x, entry_y)
                break

        elif select == 4:
            while True:
                exit_x_raw = read_until_enter("Enter new exit X: ")
                if exit_x_raw in ("\x1b", "\x03"):
                    flush()
                    return args
                exit_y_raw = read_until_enter("Enter new exit Y: ")
                if exit_y_raw in ("\x1b", "\x03"):
                    flush()
                    return args
                try:
                    exit_x = int(exit_x_raw)
                    exit_y = int(exit_y_raw)
                except ValueError:
                    print("Invalid input. Exit coordinates must be numbers.")
                    continue
                if not (0 <= exit_x < args['WIDTH']
                        and 0 <= exit_y < args['HEIGHT']):
                    print("Invalid input. Exit coordinates are out of bounds.")
                    continue
                if (exit_x, exit_y) == args['ENTRY']:
                    print("Invalid input. Exit and entry cannot be the same.")
                    continue
                args['EXIT'] = (exit_x, exit_y)
                break

        elif select == 5:
            args['PERFECT'] = not bool(args['PERFECT'])


def noargs_panel() -> int:
    try:
        box = [
            "╔═══════════════════════════════════════════════════════════════════════════════════════╗",
            "║       ___       ___       ___       ___       ___       ___       ___       ___       ║",
            "║      /\\  \\     /\\__\\     /\\  \\     /\\  \\     /\\  \\     /\\  \\     /\\__\\     /\\  \\      ║",
            "║     /  \\  \\   /  L_L_   /  \\  \\   _\\ \\  \\   /  \\  \\   _\\ \\  \\   / | _|_   /  \\  \\     ║",
            "║    /  \\ \\__\\ / /L \\__\\ /  \\ \\__\\ /    \\__\\ /  \\ \\__\\ /\\/  \\__\\ /  |/\\__\\ / /\\ \\__\\    ║",
            "║    \\/\\  /  / \\/_/ /  / \\/\\  /  / \\   _/__/ \\ \\/  / \\  /\\/__/ \\/|  /  / \\ \\/__/    ║",
            "║      / /  /    / /  /    / /  /   \\ \\__\\    \\ \\/  /   \\ \\__\\     | /  /   \\  /  /     ║",
            "║      \\/__/     \\/__/     \\/__/     \\/__/     \\/__/     \\/__/     \\/__/     \\/__/      ║",
            "╠═══════════════════════════════════════════════════════════════════════════════════════╣",
            _side_row(),
            _side_row(),
            _side_row("\033[35m► 1) default settings\033[0m", "\033[35mwritten by:\033[0m"),
            _side_row("\033[35m► 2) load parameters\033[0m", "\033[35m\033[0m"),
            _side_row("\033[35m► 3) Algorithm\033[0m", "\033[35m- alfiorav\033[0m"),
            _side_row("\033[35m► 4) run program\033[0m", "\033[35m- kr1\033[0m"),
            _side_row("\033[31m► 5) exit\033[0m", "\033[35m-\033[0m \033[34mmeow.inc\033[0m"),
            _side_row(),
            _side_row(),
            _side_row(),
            _side_row(),
            "╚═══════════════════════════════════════════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select = int(input("\033[36m►Please select an option: \033[0m"))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return panel()
    if select not in [1, 2, 3, 4, 5]:
        print("Invalid selection. Please enter 1, 2, 3, 4, or 5.")
        return panel()
    return select


def default_settings() -> dict[str, int | str | tuple[int, int]]:
    print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
    print("\033[36m║\033[35m  Using default settings                    \033[36m║\033[0m")
    print("\033[36m║  Height: 20, Width: 20                      \033[36m║\033[0m")
    print("\033[36m║  Entry: (0, 0), Exit: (19, 19)               \033[36m║\033[0m")
    print("\033[36m║  Perfect Maze: True, Algorithm: DFS         \033[36m║\033[0m")
    print("\033[36m╚════════════════════════════════════════════════╝\033[0m\n")
    return {
        'HEIGHT': 20,
        'WIDTH': 20,
        'ENTRY': (0, 0),
        'EXIT': (19, 19),
        'PERFECT': True,
        'MAZE_ANIMATION': False,
        'RES_ANIMATINON': False,
        'RANDOM_42': True,
        'SEED': None,
        'ALGORITHM': 'dfs',
    }


def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_until_enter(prompt=""):
    if prompt:
        print(prompt, end="", flush=True)
    chars = []
    while True:
        ch = get_key()
        if ch in ("\x1b", "\x03"):
            print()
            return ch
        if ch in ("\r", "\n"):
            print()
            return "".join(chars)
        if ch in ("\x7f", "\b"):
            if chars:
                chars.pop()
                print("\b \b", end="", flush=True)
            continue
        chars.append(ch)
        print(ch, end="", flush=True)


def change_params(args):
    flush()
    print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
    print("\033[36m║\033[35m  Enter Parameters                         \033[36m║\033[0m")
    print("\033[36m║\033[35m  ESC to exit dialog                       \033[36m║\033[0m")
    print("\033[36m╚════════════════════════════════════════════════╝\033[0m\n")
    try:
        while True:
            height = read_until_enter("\033[36m► Height: \033[0m")
            if height == "\x1b" or height == "\x03":
                flush()
                return args
            height = int(height)
            if height > 0 and height < 45:
                break
            print("\n\033[31m✗ Invalid input. " +
                  "Height must be between 1 and 44.\033[0m\n")

        while True:
            width = read_until_enter("\033[36m► Width: \033[0m")
            if width == "\x1b" or width == "\x03":
                flush()
                return args
            width = int(width)
            if width > 0 and width < 45:
                break
            print("\n\033[31m✗ Invalid input. " +
                  "Width must be between 1 and 44.\033[0m\n")

        while True:
            entry_x = read_until_enter("\033[36m► Entry X: \033[0m")
            if entry_x == "\x1b" or entry_x == "\x03":
                flush()
                return args
            entry_x = int(entry_x)
            entry_y = read_until_enter("\033[36m► Entry Y: \033[0m")
            if entry_y == "\x1b" or entry_y == "\x03":
                flush()
                return args
            entry_y = int(entry_y)
            if 0 <= entry_x < width and 0 <= entry_y < height:
                break
            print("\n\033[31m✗ Invalid input. " +
                  "Entry coordinates are out of bounds.\033[0m\n")

        while True:
            exit_x = read_until_enter("\033[36m► Exit X: \033[0m")
            if exit_x == "\x1b" or exit_x == "\x03":
                flush()
                return args
            exit_x = int(exit_x)
            if exit_x < 0 or exit_x >= width or exit_x == entry_x:
                print("\n\033[31m✗ Invalid input. " +
                      "Exit X coordinate is out of bounds or same as entry." +
                      "\033[0m\n")
            if 0 <= exit_x < width and exit_x != entry_x:
                break

        while True:
            exit_y = read_until_enter("\033[36m► Exit Y: \033[0m")
            if exit_y == "\x1b" or exit_y == "\x03":
                flush()
                return args
            exit_y = int(exit_y)
            if 0 <= exit_y < height and exit_y != entry_y:
                break
            if exit_y < 0 or exit_y >= height:
                print("\n\033[31m✗ Invalid input. " +
                      "Exit Y coordinate is out of bounds.\033[0m\n")
                continue

        while True:
            perfect_input = read_until_enter("\033[36m► Perfect maze (y/n): " +
                                             "\033[0m")
            if perfect_input == "\x1b" or perfect_input == "\x03":
                flush()
                return args
            perfect_input = perfect_input.strip().lower()
            if perfect_input in ['y', 'yes']:
                perfect = True
                break
            if perfect_input in ['n', 'no']:
                perfect = False
                break
            print("\n\033[31m✗ Invalid input. " +
                  "Please enter y/yes or n/no.\033[0m\n")

        flush()
        return print_promt({
            'HEIGHT': height,
            'WIDTH': width,
            'ENTRY': (entry_x, entry_y),
            'EXIT': (exit_x, exit_y),
            'PERFECT': perfect,
            'RANDOM_42': True,
            'MAZE_ANIMATION': False,
            'RES_ANIMATINON': False,
            'SEED': None,
            'ALGORITHM': 'dfs',
        })
    except (ValueError, KeyboardInterrupt, EOFError):
        print("\n\033[31m✗ Invalid input. Please enter numbers.\033[0m\n")
        return change_params(args)


def algo_panel(current_algo=None):
    def toggle(is_on):
        color = "32" if is_on else "31"
        label = "ON" if is_on else "OFF"
        return f"\033[{color}m[{label}]\033[0m"

    try:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            _box_row(),
            _box_row("             \033[36m► Select Algorithm\033[0m"),
            _box_row("      \033[33mChoose the generator to enable\033[0m"),
            _box_row(),
        ]
        for idx, (name, key) in enumerate(ALGOS, start=1):
            is_selected = (current_algo == key)
            status = toggle(is_selected)
            box.append(
                _box_row(f"  \033[35m► {idx}) {name}\033[0m  {status}")
            )
        box.extend([
            _box_row(),
            _box_row("  \033[31m► 0) back\033[0m"),
            _box_row(),
            _box_row("  \033[34mESC closes the panel too\033[0m"),
            _box_row(),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ])
        print("\n".join(box))
        select_raw = read_until_enter("\033[36m► select an algorithm\033[0m: ")
        if select_raw in ("\x1b", "\x03"):
            flush()
            return None
        select = int(select_raw)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return algo_panel(current_algo)
    if select == 0:
        return None
    if select not in range(1, len(ALGOS) + 1):
        print(f"Invalid selection. Please enter 0 to {len(ALGOS)}.")
        return algo_panel(current_algo)
    flush()
    return select


def print_promt(args: dict) -> None:
    while True:
        if args is not None:
            select = panel()
            match select:
                case 1:
                    args = params_panel(args)
                case 2:
                    flush()
                    select = algo_panel(str(args['ALGORITHM']).lower())
                    if select is None:
                        return print_promt(args)
                    args['ALGORITHM'] = ALGOS[select - 1][1]
                case 3:
                    print("Running program with current settings...")
                    from src.selection import selection_function
                    flush()
                    selection_function(args)
                case 4:
                    print("stopping program...")
                    break
        elif args is None:
            print("No arguments provided we'll use default settings, or not")
            select = noargs_panel()
            match select:
                case 1:
                    flush()
                    args = default_settings()
                    print("Default settings loaded. Returning to main menu...")
                    return print_promt(args)
                case 2:
                    change_params(args)
                case 3:
                    flush()
                    select = algo_panel(None)
                    if select is not None:
                        args['ALGORITHM'] = ALGOS[select - 1][1]  # implement variable for algo
                case 4:
                    print("Running program with current settings...")
                    from src.selection import selection_function
                    flush()
                    selection_function(default_settings())
                case 5:
                    print("stopping program...")
                    break
    flush()
