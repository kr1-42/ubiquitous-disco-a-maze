import os
import sys
import termios
import tty


def flush() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def panel() -> int:
    try:
        print(
            "╔═══════════════════════════════════════════════════════════════════════════════════════╗\n"
            "║       ___       ___       ___       ___       ___       ___       ___       ___       ║\n"
            "║      /\  \     /\__\     /\  \     /\  \     /\  \     /\  \     /\__\     /\  \      ║\n"
            "║     /::\  \   /::L_L_   /::\  \   _\:\  \   /::\  \   _\:\  \   /:| _|_   /::\  \     ║\n"
            "║    /::\:\__\ /:/L:\__\ /::\:\__\ /::::\__\ /::\:\__\ /\/::\__\ /::|/\__\ /:/\:\__\    ║\n"
            "║    \/\::/  / \/_/:/  / \/\::/  / \::;;/__/ \:\:\/  / \::/\/__/ \/|::/  / \:\:\/__/    ║\n"
            "║      /:/  /    /:/  /    /:/  /   \:\__\    \:\/  /   \:\__\     |:/  /   \::/  /     ║\n"
            "║      \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/      ║\n"
            "╠═══════════════════════════════════════════════════════════════════════════════════════╣\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║\033[35m► 1) Parameters\033[0m                                                                        ║\n"
            "║\033[35m► 2) Algoritm\033[0m                                                                          ║\n"
            "║\033[35m► 3) run program\033[0m                                                                       ║\n"
            "║\033[35m► 4) exit\033[0m                                                                              ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "╚═══════════════════════════════════════════════════════════════════════════════════════╝\n"
        )
        select = int(input("\033[36m►Please select an option: \033[0m"))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return panel()
    if select not in [1, 2, 3, 4]:
        print("Invalid selection. Please enter 1, 2, 3, or 4.")
        return panel()
    return select


def params_panel(args) -> list:
    flush()
    inside_width = 51

    def row(text=""):
        return f"║{text.ljust(inside_width)}║"

    try:
        box = [
            "╔═══════════════════════════════════════════════════╗",
            row("              \033[36m► change params\033[0m"),
            row(),
            row(f"\033[35m► 1) height\033[0m \033[32m[{args[0]}]\033[0m"),
            row(f"\033[35m► 2) width\033[0m \033[32m[{args[1]}]\033[0m"),
            row(f"\033[35m► 3) entry\033[0m \033[32m[{args[2]}]\033[0m"),
            row(f"\033[35m► 4) exit\033[0m \033[32m[{args[3]}]\033[0m"),
            row(f"\033[35m► 5) perfect\033[0m \033[32m[{args[4]}]\033[0m"),
            row(),
            row("\033[31m► 0) back\033[0m"),
            row(),
            row(),
            row(),
            row(),
            "╚═══════════════════════════════════════════════════╝",
            "",
        ]
        print("\n".join(box))
        select_raw = read_until_enter("\033[36m► select an option\033[0m: ")
        if select_raw in ("\x1b", "\x03"):
            flush()
            return args
        select = int(select_raw)
    except ValueError:
        print("Invalid input. Please enter a number.")
        return params_panel(args)
    if select not in [0, 1, 2, 3, 4, 5]:
        print("Invalid selection. Please enter a number between 0 and 5.")
        return params_panel(args)
    if select == 0:
        flush()
        return args
    match select:
        case 1:
            print(f"\nCurrent height: {args[0]}\n")
            try:
                height = read_until_enter("Enter new height: ")
                if height in ("\x1b", "\x03"):
                    flush()
                    return args
                args[0] = int(height)
            except ValueError:
                print("Invalid input. Please enter a number.")
                return params_panel(args)
        case 2:
            print(f"\nCurrent width: {args[1]}\n")
            try:
                width = read_until_enter("Enter new width: ")
                if width in ("\x1b", "\x03"):
                    flush()
                    return args
                args[1] = int(width)
            except ValueError:
                print("Invalid input. Please enter a number.")
                return params_panel(args)
        case 3:
            print(f"\nCurrent entry point: {args[2]}\n")
            try:
                entry_input = read_until_enter("Enter new entry point x: ")
                if entry_input in ("\x1b", "\x03"):
                    flush()
                    return args
                entry_y_input = read_until_enter("Enter new entry point y: ")
                if entry_y_input in ("\x1b", "\x03"):
                    flush()
                    return args
                args[2] = (int(entry_input), int(entry_y_input))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                return params_panel(args)
        case 4:
            print(f"\nCurrent exit point: {args[3]}\n")
            try:
                exit_input = read_until_enter("Enter new exit point x: ")
                if exit_input in ("\x1b", "\x03"):
                    flush()
                    return args
                exit_y_input = read_until_enter("Enter new exit point y: ")
                if exit_y_input in ("\x1b", "\x03"):
                    flush()
                    return args
                args[3] = (int(exit_input), int(exit_y_input))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                return params_panel(args)
        case 5:
            print(f"\nCurrent perfect setting: {args[4]}\n")
            perfect_input = read_until_enter("Should the maze be perfect? (y/n): ")
            if perfect_input in ("\x1b", "\x03"):
                flush()
                return args
            if perfect_input.lower() in ['y', 'yes']:
                args[4] = True
            elif perfect_input.lower() in ['n', 'no']:
                args[4] = False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                return params_panel(args)
    flush()
    return args


def noargs_panel() -> int:
    try:
            print(
            "╔═══════════════════════════════════════════════════════════════════════════════════════╗\n"
            "║       ___       ___       ___       ___       ___       ___       ___       ___       ║\n"
            "║      /\  \     /\__\     /\  \     /\  \     /\  \     /\  \     /\__\     /\  \      ║\n"
            "║     /  \  \   /  L_L_   /  \  \   _\ \  \   /  \  \   _\ \  \   / | _|_   /  \  \     ║\n"
            "║    /  \ \__\ / /L \__\ /  \ \__\ /    \__\ /  \ \__\ /\/  \__\ /  |/\__\ / /\ \__\    ║\n"
            "║    \/\  /  / \/_/ /  / \/\  /  / \   _/__/ \ \ \/  / \  /\/__/ \/|  /  / \ \ \/__/    ║\n"
            "║      / /  /    / /  /    / /  /   \ \__\    \ \/  /   \ \__\     | /  /   \  /  /     ║\n"
            "║      \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/     \/__/      ║\n"
            "╠═══════════════════════════════════════════════════════════════════════════════════════╣\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║\033[35m► 1) default settings\033[0m                                                                  ║\n"
            "║\033[35m► 2) load parameters\033[0m                                                                   ║\n"
            "║\033[35m► 3) Algoritm\033[0m                                                                          ║\n"
            "║\033[35m► 4) run program\033[0m                                                                       ║\n"
            "║\033[35m► 5) exit\033[0m                                                                              ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "╚═══════════════════════════════════════════════════════════════════════════════════════╝\n"
            )
            select = int(input("\033[36m►Please select an option: \033[0m"))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return panel()
    if select not in [1, 2, 3, 4, 5]:
        print("Invalid selection. Please enter 1, 2, 3, 4, or 5.")
        return panel()
    return select


def default_settings() -> list:
    print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
    print("\033[36m║\033[35m  Using default settings                    \033[36m║\033[0m")
    print("\033[36m║  Height: 20, Width: 20                      \033[36m║\033[0m")
    print("\033[36m║  Entry: (0, 0), Exit: (19, 19)               \033[36m║\033[0m")
    print("\033[36m║  Perfect Maze: True, Algorithm: DFS         \033[36m║\033[0m")
    print("\033[36m╚════════════════════════════════════════════════╝\033[0m\n")
    return [20, 20, (0, 0), (19, 19), True, None, 'dfs']


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
            print("\n\033[31m✗ Invalid input. Height must be between 1 and 44.\033[0m\n")

        while True:
            width = read_until_enter("\033[36m► Width: \033[0m")
            if width == "\x1b" or width == "\x03":
                flush()
                return args
            width = int(width)
            if width > 0 and width < 45:
                break
            print("\n\033[31m✗ Invalid input. Width must be between 1 and 44.\033[0m\n")

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
            print("\n\033[31m✗ Invalid input. Entry coordinates are out of bounds.\033[0m\n")

        while True:
            exit_x = read_until_enter("\033[36m► Exit X: \033[0m")
            if exit_x == "\x1b" or exit_x == "\x03":
                flush()
                return args
            exit_x = int(exit_x)
            if exit_x < 0 or exit_x >= width or exit_x == entry_x:
                print("\n\033[31m✗ Invalid input. Exit X coordinate is out of bounds or same as entry.\033[0m\n")
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
                print("\n\033[31m✗ Invalid input. Exit Y coordinate is out of bounds.\033[0m\n")
                continue

        while True:
            perfect_input = read_until_enter("\033[36m► Perfect maze (y/n): \033[0m")
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
            print("\n\033[31m✗ Invalid input. Please enter y/yes or n/no.\033[0m\n")

        flush()
        return print_promt([
            height,
            width,
            (entry_x, entry_y),
            (exit_x, exit_y),
            perfect,
            None,
            'dfs',
        ])
    except (ValueError, KeyboardInterrupt, EOFError):
        print("\n\033[31m✗ Invalid input. Please enter numbers.\033[0m\n")
        return change_params(args)


def print_promt(args=None):
    while True:
        if args is not None:
            select = panel()
            match select:
                case 1:
                    args = params_panel(args)
                case 2:
                    print("Algorithm selection not implemented yet.")
                    return print_promt(args)
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
                    from src.selection import selection_function
                    return selection_function(default_settings())
                case 2:
                    change_params(args)
                case 3:
                    print("Algorithm selection not implemented yet.")
                case 4:
                    print("Running program with current settings...")
                    from src.selection import selection_function
                    flush()
                    selection_function(default_settings())
                case 5:
                    print("stopping program...")
                    break
    flush()


