import os
import re
import sys
import termios
import tty
from typing import TypedDict


ANSI_RE = re.compile(r"\x1b\[[0-9;]*m")
CANCEL_SIGNALS = ("\x1b", "\x03")

ALGOS = [
    ("Backtracking Algorithm", "back"),
    ("Prim's Algorithm", "prim"),
    ("Recursive Division Algorithm (extra)", "div"),
]


class MazeArgs(TypedDict):
    HEIGHT: int
    WIDTH: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool
    ALGORITHM: str
    ANIMATION_SPEED: float
    MAZE_ANIMATION: bool
    RES_ANIMATINON: bool
    RANDOM_42: bool
    SEED: int | None


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


def _format_param_value(value: object) -> str:
    if isinstance(value, bool):
        color = "32" if value else "31"
        label = "ON" if value else "OFF"
        return f"\033[{color}m[{label}]\033[0m"
    return f"\033[36m[{value}]\033[0m"


def _is_cancel_signal(value: str) -> bool:
    return value in CANCEL_SIGNALS


def flush() -> None:
    os.system("cls" if os.name == "nt" else "clear")


def panel() -> int:
    while True:
        box = [
            (
                "╔════════════════════════════════════════"
                "═══════════════════════════════════════════════╗"
            ),
            (
                "║       ___       ___       ___       ___     "
                "  ___       ___       ___       ___       ║"
            ),
            (
                "║      /\\  \\     /\\__\\     /\\  \\     /\\  \\ "
                "    /\\  \\     /\\  \\     /\\__\\     /\\  \\      ║"
            ),
            (
                "║     /  \\  \\   /  L_L_   /  \\  \\   _\\ \\  \\ "
                "  /  \\  \\   _\\ \\  \\   / | _|_   /  \\  \\     ║"
            ),
            (
                "║    /  \\ \\__\\ / /L \\__\\ /  \\ \\__\\ /    \\__\\ "
                "/  \\ \\__\\ /\\/  \\__\\ /  |/\\__\\ / /\\ \\__\\    ║"
            ),
            (
                "║    \\/\\  /  / \\/_/ /  / \\/\\  /  / \\  __/__/ "
                "\\ \\ \\/  / \\  /\\/__/ \\/|  /  / \\ \\ \\/__/    ║"
            ),
            (
                "║      / /  /    / /  /    / /  /   \\ \\__\\    "
                "\\ \\/  /   \\ \\__\\     | /  /   \\  /  /     ║"
            ),
            (
                "║      \\/__/     \\/__/     \\/__/     \\/__/     "
                "\\/__/     \\/__/     \\/__/     \\/__/      ║"
            ),
            (
                "╠════════════════════════════════════════"
                "═══════════════════════════════════════════════╣"
            ),
            _side_row(),
            _side_row(),
            _side_row(
                "\033[35m► 1) Parameters\033[0m",
                "\033[35mwritten by:\033[0m",
            ),
            _side_row("\033[35m► 2) Algorithm\033[0m", "\033[35m\033[0m"),
            _side_row("\033[31m► 3) choose seed\033[0m", "\033[35m\033[0m"),
            _side_row(
                "\033[35m► 4) run program\033[0m",
                "\033[35m- alfiorav\033[0m",
            ),
            _side_row("\033[31m► 5) exit\033[0m", "\033[35m- kr1\033[0m"),
            _side_row("", "\033[35m-\033[0m \033[34mmeow.inc\033[0m"),
            _side_row(),
            _side_row(),
            _side_row(),
            _side_row(),
            (
                "╚════════════════════════════════════════"
                "═══════════════════════════════════════════════╝"
            ),
            "",
        ]
        print("\n".join(box))

        try:
            select = int(input("\033[36m►Please select an option: \033[0m"))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if select in [1, 2, 3, 4, 5]:
            return select
        print("Invalid selection. Please enter 1, 2, 3, 4, or 5.")


def noargs_panel() -> int:
    while True:
        box = [
            (
                "╔════════════════════════════════════════"
                "═══════════════════════════════════════════════╗"
            ),
            (
                "║       ___       ___       ___       ___     "
                "  ___       ___       ___       ___       ║"
            ),
            (
                "║      /\\  \\     /\\__\\     /\\  \\     /\\  \\ "
                "    /\\  \\     /\\  \\     /\\__\\     /\\  \\      ║"
            ),
            (
                "║     /  \\  \\   /  L_L_   /  \\  \\   _\\ \\  \\ "
                "  /  \\  \\   _\\ \\  \\   / | _|_   /  \\  \\     ║"
            ),
            (
                "║    /  \\ \\__\\ / /L \\__\\ /  \\ \\__\\ /    \\__\\ "
                "/  \\ \\__\\ /\\/  \\__\\ /  |/\\__\\ / /\\ \\__\\    ║"
            ),
            (
                "║    \\/\\  /  / \\/_/ /  / \\/\\  /  / \\  __/__/ "
                "\\ \\ \\/  / \\  /\\/__/ \\/|  /  / \\ \\ \\/__/    ║"
            ),
            (
                "║      / /  /    / /  /    / /  /   \\ \\__\\    "
                "\\ \\/  /   \\ \\__\\     | /  /   \\  /  /     ║"
            ),
            (
                "║      \\/__/     \\/__/     \\/__/     \\/__/     "
                "\\/__/     \\/__/     \\/__/     \\/__/      ║"
            ),
            (
                "╠════════════════════════════════════════"
                "═══════════════════════════════════════════════╣"
            ),
            _side_row(),
            _side_row(),
            _side_row(
                "\033[35m► 1) default settings\033[0m",
                "\033[35mwritten by:\033[0m",
            ),
            _side_row(
                "\033[35m► 2) load parameters\033[0m",
                "\033[35m\033[0m",
            ),
            _side_row(
                "\033[35m► 3) Algorithm\033[0m",
                "\033[35m- alfiorav\033[0m",
            ),
            _side_row("\033[35m► 4) seed\033[0m", "\033[35m\033[0m"),
            _side_row(
                "\033[35m► 5) run program\033[0m",
                "\033[35m- kr1\033[0m",
            ),
            _side_row(
                "\033[31m► 6) exit\033[0m",
                "\033[35m-\033[0m \033[34mmeow.inc\033[0m",
            ),
            _side_row(),
            _side_row(),
            _side_row(),
            _side_row(),
            (
                "╚════════════════════════════════════════"
                "═══════════════════════════════════════════════╝"
            ),
            "",
        ]
        print("\n".join(box))

        try:
            select = int(input("\033[36m►Please select an option: \033[0m"))
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if select in [1, 2, 3, 4, 5, 6]:
            return select
        print("Invalid selection. Please enter 1, 2, 3, 4, or 5 or 6.")


def default_settings() -> MazeArgs:
    print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
    print(
        "\033[36m║\033[35m  Using default settings                    "
        "\033[36m║\033[0m"
    )
    print(
        "\033[36m║  Height: 20, Width: 20                      "
        "\033[36m║\033[0m"
    )
    print(
        "\033[36m║  Entry: (0, 0), Exit: (19, 19)               "
        "\033[36m║\033[0m"
    )
    print(
        "\033[36m║  Perfect Maze: True, Algorithm: DFS         "
        "\033[36m║\033[0m"
    )
    print(
        "\033[36m╚════════════════════════════════════════════════╝"
        "\033[0m\n"
    )
    return {
        'HEIGHT': 20,
        'WIDTH': 20,
        'ENTRY': (0, 0),
        'EXIT': (19, 19),
        'PERFECT': True,
        'ALGORITHM': 'back',
        'ANIMATION_SPEED': 0.5,
        'MAZE_ANIMATION': False,
        'RES_ANIMATINON': False,
        'RANDOM_42': False,
        'SEED': None,
        'COLOR': 'default'
        }




def get_key() -> str:
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


def read_until_enter(prompt: str = "") -> str:
    if prompt:
        print(prompt, end="", flush=True)
    chars: list[str] = []

    while True:
        ch = get_key()
        if _is_cancel_signal(ch):
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


def _ask_size(prompt: str, axis_name: str) -> int | None:
    while True:
        raw = read_until_enter(prompt)
        if _is_cancel_signal(raw):
            return None
        try:
            value = int(raw)
        except ValueError:
            print(f"Invalid input. {axis_name} must be a number.")
            continue
        if 9 <= value <= 44:
            return value
        print(f"Invalid input. {axis_name} must be between 9 and 44.")


def _ask_point(label: str) -> tuple[int, int] | None:
    while True:
        x_raw = read_until_enter(f"Enter new {label} X: ")
        if _is_cancel_signal(x_raw):
            return None

        y_raw = read_until_enter(f"Enter new {label} Y: ")
        if _is_cancel_signal(y_raw):
            return None

        try:
            return (int(x_raw), int(y_raw))
        except ValueError:
            print(
                f"Invalid input. {label.capitalize()} coordinates "
                "must be numbers."
            )


def params_panel(args: MazeArgs) -> MazeArgs:
    while True:
        flush()
        box = [
            "╔═══════════════════════════════════════════════════╗",
            _box_row(),
            _box_row("              \033[36m► Change Params\033[0m"),
            _box_row("      \033[33mValidate values before generate\033[0m"),
            _box_row(),
            _box_row(
                f"  \033[35m► 1) height\033[0m   "
                f"{_format_param_value(args['HEIGHT'])}"
            ),
            _box_row(
                f"  \033[35m► 2) width\033[0m    "
                f"{_format_param_value(args['WIDTH'])}"
            ),
            _box_row(
                f"  \033[35m► 3) entry\033[0m    "
                f"{_format_param_value(args['ENTRY'])}"
            ),
            _box_row(
                f"  \033[35m► 4) exit\033[0m     "
                f"{_format_param_value(args['EXIT'])}"
            ),
            _box_row(
                f"  \033[35m► 5) seed\033[0m     "
                f"{_format_param_value(args['SEED'])}"
            ),
            _box_row(
                f"  \033[35m► 6) perfect\033[0m  "
                f"{_format_param_value(args['PERFECT'])}"
            ),
            _box_row(
                f"  \033[35m► 7) maze_animation\033[0m     "
                f"{_format_param_value(args['MAZE_ANIMATION'])}"
            ),
            _box_row(
                f"  \033[35m► 8) res_animation\033[0m     "
                f"{_format_param_value(args['RES_ANIMATINON'])}"
            ),
            _box_row(
                f"  \033[35m► 9) random_42\033[0m     "
                f"{_format_param_value(args['RANDOM_42'])}"
            ),
            _box_row(),
            _box_row("  \033[31m► 0) back\033[0m"),
            _box_row(),
            _box_row(
                "  \033[34mRanges: size 1-44, points must be "
                "in bounds\033[0m"
            ),
            _box_row("  \033[34mESC closes the panel too\033[0m"),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))

        select_raw = read_until_enter("\033[36m► select an option\033[0m: ")
        if _is_cancel_signal(select_raw):
            flush()
            return args

        try:
            select = int(select_raw)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if select == 0:
            flush()
            return args

        if select == 1:
            height = _ask_size("Enter new height (1-44): ", "Height")
            if height is None:
                flush()
                return args
            if height < 7 and\
                    (args["ENTRY"][1] >= height or args["EXIT"][1] >= height):
                print(
                    "Invalid input. Entry/exit Y out of bounds for small mazes"
                    )
                continue
            if args["ENTRY"][1] >= height and args["EXIT"][1] >= height:
                print("Invalid input. Entry/exit Y out of bounds.")
                continue
            args["HEIGHT"] = height
            continue

        if select == 2:
            width = _ask_size("Enter new width (1-44): ", "Width")
            if width is None:
                flush()
                return args
            if width < 10 and\
                    (args["ENTRY"][0] >= width or args["EXIT"][0] >= width):
                print(
                    "Invalid input. Entry/exit X out of bounds for small mazes"
                    )
                continue
            if args["ENTRY"][0] >= width and args["EXIT"][0] >= width:
                print("Invalid input. Entry/exit X out of bounds.")
                continue
            args["WIDTH"] = width
            continue

        if select == 3:
            entry = _ask_point("entry")
            if entry is None:
                flush()
                return args
            if not (
                0 <= entry[0] < args["WIDTH"]
                and 0 <= entry[1] < args["HEIGHT"]
            ):
                print("Invalid input. Entry is out of bounds.")
                continue
            if entry == args["EXIT"]:
                print("Invalid input. Entry and exit cannot be the same.")
                continue
            args["ENTRY"] = entry
            continue

        if select == 4:
            exit_point = _ask_point("exit")
            if exit_point is None:
                flush()
                return args
            if not (
                0 <= exit_point[0] < args["WIDTH"]
                and 0 <= exit_point[1] < args["HEIGHT"]
            ):
                print("Invalid input. Exit coordinates are out of bounds.")
                continue
            if exit_point == args["ENTRY"]:
                print("Invalid input. Exit and entry cannot be the same.")
                continue
            args["EXIT"] = exit_point
            continue

        if select == 5:
            seed_raw = read_until_enter(
                "Enter new seed (integer or empty to unset): "
            )
            if _is_cancel_signal(seed_raw):
                flush()
                return args
            args["SEED"] = (
                int(seed_raw) if seed_raw.isdigit() else seed_raw.__hash__()
            )
            continue
        if select == 6:
            args["PERFECT"] = not args["PERFECT"]
            continue
        if select == 7:
            args["MAZE_ANIMATION"] = not args["MAZE_ANIMATION"]
            continue
        if select == 8:
            args["RES_ANIMATINON"] = not args["RES_ANIMATINON"]
            continue
        if select == 9:
            args["RANDOM_42"] = not args["RANDOM_42"]
            continue
        print("Invalid selection. Please enter a number between 0 and 9.")


def change_params(args: MazeArgs | None) -> MazeArgs:
    flush()
    print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
    print(
        "\033[36m║\033[35m  Enter Parameters                         "
        "\033[36m║\033[0m"
    )
    print(
        "\033[36m║\033[35m  ESC to exit dialog                       "
        "\033[36m║\033[0m"
    )
    print(
        "\033[36m╚════════════════════════════════════════════════╝"
        "\033[0m\n"
    )

    base_args = args or default_settings()
    return params_panel(base_args)


def algo_panel(current_algo: str | None = None) -> int | None:
    def toggle(is_on: bool) -> str:
        color = "32" if is_on else "31"
        label = "ON" if is_on else "OFF"
        return f"\033[{color}m[{label}]\033[0m"

    while True:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            _box_row(),
            _box_row("             \033[36m► Select Algorithm\033[0m"),
            _box_row("      \033[33mChoose the generator to enable\033[0m"),
            _box_row(),
        ]
        for idx, (name, key) in enumerate(ALGOS, start=1):
            status = toggle(current_algo == key)
            box.append(_box_row(f"  \033[35m► {idx}) {name}\033[0m  {status}"))

        box.extend(
            [
                _box_row(),
                _box_row("  \033[31m► 0) back\033[0m"),
                _box_row(),
                _box_row("  \033[34mESC closes the panel too\033[0m"),
                _box_row(),
                "╚═══════════════════════════════════════════════════╝",
                "",
            ]
        )
        print("\n".join(box))

        select_raw = read_until_enter("\033[36m► select an algorithm\033[0m: ")
        if _is_cancel_signal(select_raw):
            flush()
            return None

        try:
            select = int(select_raw)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if select == 0:
            return None
        if select in range(1, len(ALGOS) + 1):
            flush()
            return select

        print(f"Invalid selection. Please enter 0 to {len(ALGOS)}.")


def print_promt(args: MazeArgs) -> None:
    while True:
        if args is None:
            print("No arguments provided we'll use default settings, or not")
            select = noargs_panel()

            if select == 1:
                flush()
                args = default_settings()
                print("Default settings loaded. Returning to main menu...")
                continue

            if select == 2:
                args = change_params(default_settings())
                continue

            if select == 3:
                selected_algo = algo_panel(None)
                if selected_algo is not None:
                    args = default_settings()
                    args["ALGORITHM"] = ALGOS[selected_algo - 1][1]
                continue

            if select == 4:
                seed_raw = read_until_enter(
                    "Enter new seed (integer or empty to unset): "
                )
                if _is_cancel_signal(seed_raw):
                    flush()
                    continue
                if args is None:
                    args = default_settings()
                args["SEED"] = (
                    int(seed_raw)
                    if seed_raw.isdigit()
                    else seed_raw.__hash__()
                )
                continue

            if select == 5:
                print("Running program with current settings...")
                from src.selection import selection_function

                flush()
                selection_function(default_settings())
                continue

            if select == 6:
                print("stopping program...")
                break

        else:
            select = panel()

            if select == 1:
                args = params_panel(args)
                continue

            if select == 2:
                flush()
                selected_algo = algo_panel(str(args["ALGORITHM"]).lower())
                if selected_algo is not None:
                    args["ALGORITHM"] = ALGOS[selected_algo - 1][1]
                continue
            if select == 3:
                seed_raw = read_until_enter(
                    "Enter new seed (integer or empty to unset): "
                )
                if _is_cancel_signal(seed_raw):
                    flush()
                    continue
                args["SEED"] = (
                    int(seed_raw)
                    if seed_raw.isdigit()
                    else seed_raw.__hash__()
                )
                continue
            if select == 4:
                print("Running program with current settings...")
                from src.selection import selection_function

                flush()
                selection_function(args)
                continue
            if select == 5:
                print("stopping program...")
                break

    flush()
