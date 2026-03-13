import os

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


def params_panel(args) -> int:
    flush()
    try:
        print(
            "╔═══════════════════════════════════════════════════╗\n"
            "║              \033[36m► change params\033[0m                      ║\n"
            "║                                                   ║\n"
            "║\033[35m► 1) height\033[0m                                        ║\n"
            "║\033[35m► 2) width\033[0m                                         ║\n"
            "║\033[35m► 3) entry\033[0m                                         ║\n"
            "║\033[35m► 4) exit\033[0m                                          ║\n"
            "║\033[35m► 5) perfect\033[0m                                       ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "╚═══════════════════════════════════════════════════╝\n"
                )
        select = int(input("\033[36m► select an option\033[0m: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return params_panel(args)
    if select not in [1, 2, 3, 4, 5]:
        print("Invalid selection. Please enter a number between 1 and 5.")
        return params_panel(args)
    match select:
        case 1:
            print(f"\nCurrent height: {args[0]}\n")
            try:
                args[0] = int(input("Enter new height: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                return params_panel(args)
        case 2:
            print(f"\nCurrent width: {args[1]}\n")
            try:
                args[1] = int(input("Enter new width: "))
            except ValueError:
                print("Invalid input. Please enter a number.")
                return params_panel(args)
        case 3:
            print(f"\nCurrent entry point: {args[2]}\n")
            try:
                entry_input = input("Enter new entry point x: ")
                entry_y_input = input("Enter new entry point y: ")
                args[2] = (int(entry_input), int(entry_y_input))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                return params_panel(args)
        case 4:
            print(f"\nCurrent exit point: {args[3]}\n")
            try:
                exit_input = input("Enter new exit point x: ")
                exit_y_input = input("Enter new exit point y: ")
                args[3] = (int(exit_input), int(exit_y_input))
            except ValueError:
                print("Invalid input. Please enter numbers.")
                return params_panel(args)
        case 5:
            print(f"\nCurrent perfect setting: {args[4]}\n")
            perfect_input = input("Should the maze be perfect? (y/n): ")
            if perfect_input.lower() in ['y', 'yes']:
                args[4] = True
            elif perfect_input.lower() in ['n', 'no']:
                args[4] = False
            else:
                print("Invalid input. Please enter 'y' or 'n'.")
                return params_panel(args)
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


def change_params(args) -> list:
        print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
        print("\033[36m║\033[35m  Enter Parameters                         \033[36m║\033[0m")
        print("\033[36m╚════════════════════════════════════════════════╝\033[0m\n")
        try:
            while True:
                height = int(input("\033[36m► Height: \033[0m"))
                if height > 0 and height < 45:
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Height must be between 1 and 44.\033[0m\n")
            while True:
                width = int(input("\033[36m► Width: \033[0m"))
                if width > 0 and width < 45:
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Width must be between 1 and 44.\033[0m\n")
            while True:
                entry_x = int(input("\033[36m► Entry X: \033[0m"))
                entry_y = int(input("\033[36m► Entry Y: \033[0m"))
                if 0 <= entry_x < width and 0 <= entry_y < height:
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Entry coordinates are out of bounds.\033[0m\n")
            while True:
                exit_x = int(input("\033[36m► Exit X: \033[0m"))
                exit_y = int(input("\033[36m► Exit Y: \033[0m"))
                if 0 <= exit_x < width and 0 <= exit_y < height:
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Exit coordinates are out of bounds.\033[0m\n")
            while True:
                perfect_input = input("\033[36m► Perfect maze (y/n): \033[0m").strip().lower()
                if perfect_input in ['y', 'yes']:
                    perfect = True
                    break
                elif perfect_input in ['n', 'no']:
                    perfect = False
                    break
                else:
                    print("\n\033[31m✗ Invalid input. Please enter y/yes or n/no.\033[0m\n")
            return print_promt([height, width, (entry_x, entry_y), (exit_x, exit_y), perfect, None, 'dfs'])
        except ValueError:
            print("\n\033[31m✗ Invalid input. Please enter numbers."
                  "\033[0m\n")
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
                    return default_settings()
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


