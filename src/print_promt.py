import os


def flush() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')


def panel() -> int:
    flush()
    try:
        select = int(input(
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
            "║\033[35m► 3) run program\033[0m                                                                          ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "╚═══════════════════════════════════════════════════════════════════════════════════════╝\n"
            "\033[36m►Please select an option: \033[0m"
        ))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return panel()
    if select not in [1, 2, 3]:
        print("Invalid selection. Please enter 1, 2, or 3.")
        return panel()
    return select

def params_panel(args) -> int:
    flush()
    try:
        select = int(input(
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
            "\033[36m► select an option\033[0m: "
                ))
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
    flush()
    try:
        select = int(input(
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
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "╚═══════════════════════════════════════════════════════════════════════════════════════╝\n"
            "\033[36m►Please select an option: \033[0m"
        ))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return panel()
    if select not in [1, 2, 3, 4]:
        print("Invalid selection. Please enter 1, 2, 3, or 4.")
        return panel()
    return select

def print_promt(args=None):
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
                return args
    elif args is None:
        print("No arguments provided we'll use default settings, or not")
        select = noargs_panel()
        flush()
        match select:
            case 1:
                print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
                print("\033[36m║\033[35m  Using default settings                    \033[36m║\033[0m")
                print("\033[36m║  Height: 20, Width: 20                      \033[36m║\033[0m")
                print("\033[36m║  Entry: (0, 0), Exit: (19, 19)               \033[36m║\033[0m")
                print("\033[36m║  Perfect Maze: True, Algorithm: DFS         \033[36m║\033[0m")
                print("\033[36m╚════════════════════════════════════════════════╝\033[0m\n")
                return [20, 20, (0, 0), (19, 19), False, True, True, 'dfs']
            case 2:
                print("\033[36m╔════════════════════════════════════════════════╗\033[0m")
                print("\033[36m║\033[35m  Enter Parameters                         \033[36m║\033[0m")
                print("\033[36m╚════════════════════════════════════════════════╝\033[0m\n")
                try:
                    height = int(input("\033[36m► Height: \033[0m"))
                    width = int(input("\033[36m► Width: \033[0m"))
                    entry_x = int(input("\033[36m► Entry X: \033[0m"))
                    entry_y = int(input("\033[36m► Entry Y: \033[0m"))
                    exit_x = int(input("\033[36m► Exit X: \033[0m"))
                    exit_y = int(input("\033[36m► Exit Y: \033[0m"))
                    perfect_input = input(
                        "\033[36m► Perfect maze? (y/n): \033[0m"
                    )
                    animation_input = input(
                        "\033[36m► Animation enabled? (y/n): \033[0m"
                    )
                    random_42_input = input(
                        "\033[36m► Random 42 location enabled? (y/n): \033[0m"
                    )
                    perfect = False
                    if perfect_input.lower() in ['y', 'yes'] == 'y':
                        perfect = True
                    animation = False
                    if animation_input.lower() in ['y', 'yes'] == 'y':
                        animation = True
                    random_42 = False
                    if random_42_input.lower() in ['y', 'yes'] == 'y':
                        random_42 = True
                    return print_promt([height, width, (entry_x, entry_y), (exit_x, exit_y), perfect, animation, random_42, 'dfs'])
                except ValueError:
                    print("\n\033[31m✗ Invalid input. Please enter numbers."
                          "\033[0m\n")
                    return print_promt()
            case 3:
                print("Algorithm selection not implemented yet.")
            case 4:
                print("Running program with current settings...")




