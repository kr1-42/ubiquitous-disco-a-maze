from maze import Maze

def selection_function(cols, rows):
    random_42 = True
    start = (0, 0)
    end = (21, 21)
    m = Maze(cols, rows, start, end)
    start_row, start_col = m.start
    end_row, end_col = m.end
    m.grid[start_row][start_col].start = True
    m.grid[end_row][end_col].end = True
    if random_42 is True:
        m.random_draw_42(cols, rows)
    else:
        m.draw_42(cols, rows)
    m.backtracking(m.grid[0][0], True, True)
    m.bfs(True)
    m.print_maze()
    m.print_hexa_maze("hexa.txt")
    print('\033[3J\033[H')


selection_function(22, 22)


""" def selection_function(cols, rows):
    while True:
        print("\033[2J\033[H", end="")
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
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "║                                                                                       ║\n"
            "╚═══════════════════════════════════════════════════════════════════════════════════════╝"
        ))
        match select:
            case 1:
                select = int(input(
            "╔═══════════════════════════════════════════════════╗\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║\033[35m► 1) Parameters\033[0m                                    ║\n"
            "║\033[35m► 2) Algoritm\033[0m                                      ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "╚═══════════════════════════════════════════════════╝"
                ))
            case 2:
                select = int(input(
            "╔═══════════════════════════════════════════════════╗\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║\033[35m► 1) Backtracking\033[0m                                    ║\n"
            "║\033[35m► 2) Prim\033[0m                                      ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "║                                                   ║\n"
            "╚═══════════════════════════════════════════════════╝"
                ))


def initialization_funcion(cols, rows):
    start = (3, 3)
    end = (17, 17)
    m = Maze(cols, rows, start, end)
    m.draw_42(cols, rows)
    m.print_maze() """


""" initialization_funcion(11, 11) """

