from cell import Cell
from time import sleep
import random


class Maze:
    def __init__(self, rows, cols):
        self.rows = rows
        self.cols = cols
        self.grid = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

    def print_maze(self):
        print('\033[3J\033[H')
        wall = "\033[48;2;254;254;254m  \033[0m"
        path = "\033[48;2;0;0;0m  \033[0m"
        wall_42 = "\033[48;2;255;0;0m  \033[0m"
        path_42 = "\033[48;2;255;0;0m  \033[0m"
        print(wall * (self.cols * 2 + 1))
        for r in self.grid:
            line = wall
            bottom = wall
            for c in r:
                if c._42:
                    line += path_42
                    if self.grid[c.row][c.col + 1]._42:
                        line += wall_42
                    else:
                        line += wall
                    if self.grid[c.row + 1][c.col]._42:
                        bottom += wall_42
                    else:
                        bottom += wall
                else:
                    line += path
                    if c.east:
                        line += wall
                    else:
                        line += path
                    if c.south:
                        bottom += wall
                    else:
                        bottom += path        
                bottom += wall
            print(line)
            print(bottom)
        sleep(0.005)

    def draw_42(self, center_row, center_col):
        pattern = [
            "#   ###",
            "#     #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]

        """ pattern1 = [
            "# ###",
            "# #  ",
            "#####",
            "  # #",
            "### #"
        ]
        pattern2 = [
            " ## ## ",
            "#######",
            " ##### ",
            "  ###  ",
            "   #   "
        ]
        pattern3 = [
            "   #   ",
            "   #   ",
            " ##### ",
            " ####  ",
            "  ##   "
        ] """

        start_row = center_row - 4 // 2
        start_col = center_col - 6 // 2
        """ start_row = center_row - 5 // 2
        start_col = center_col - 5 // 2 """
        for r , row in enumerate(pattern):
            for c , ch in enumerate(row):
                if ch == "#":
                    self.grid[start_row + r][start_col + c].visited = True
                    self.grid[start_row + r][start_col + c]._42 = True
                    
    def animated_backtracking(self, starting_cell=None):
        stack = []
        curr_cell = starting_cell
        curr_cell.visited = 1
        while self.has_unvisited_cells():
            unvisited = self.unvisited_neighbours(curr_cell)
            if unvisited:
                direction = random.choice(unvisited)
                curr_cell.break_wall(direction)
                
                direction.visited = 1
                if self.unvisited_neighbours(curr_cell):
                    stack.append(curr_cell)
                curr_cell = direction
            else:
                curr_cell = stack.pop()
            self.print_maze()

    def backtracking(self, starting_cell=None):
        stack = []
        curr_cell = starting_cell
        curr_cell.visited = 1
        while self.has_unvisited_cells():
            unvisited = self.unvisited_neighbours(curr_cell)
            if unvisited:
                direction = random.choice(unvisited)
                curr_cell.break_wall(direction)
                
                direction.visited = 1
                if self.unvisited_neighbours(curr_cell):
                    stack.append(curr_cell)
                curr_cell = direction
            else:
                curr_cell = stack.pop()

    def animated_bad_backtracking(self, starting_cell=None):
        stack = []
        curr_cell = starting_cell
        curr_cell.visited = 1
        while self.has_unvisited_cells():
            unvisited = self.unvisited_neighbours(curr_cell)
            if unvisited:
                direction = random.choice(unvisited)
                curr_cell.break_wall(direction)
                direction.visited = random.randint(0, 1) < 0.5
                if self.unvisited_neighbours(curr_cell):
                    stack.append(curr_cell)
                curr_cell = direction
            else:
                curr_cell = stack.pop()
            self.print_maze()

    def has_unvisited_cells(self) -> bool:
        for r in self.grid:
            for c in r:
                if not c.visited:
                    return True
        return False

    def unvisited_neighbours(self, cell) -> list:
        unvisited = []
        if cell.row > 0 and not self.grid[cell.row - 1][cell.col].visited:
            unvisited.append(self.grid[cell.row - 1][cell.col])
        if cell.row < self.rows - 1 and not self.grid[cell.row + 1][cell.col].visited:
            unvisited.append(self.grid[cell.row + 1][cell.col])
        if cell.col < self.cols - 1 and not self.grid[cell.row][cell.col + 1].visited:
            unvisited.append(self.grid[cell.row][cell.col + 1])
        if cell.col > 0 and not self.grid[cell.row][cell.col - 1].visited:
            unvisited.append(self.grid[cell.row][cell.col - 1])
        return unvisited


    def prim_algoritm(self, starting_cell=None):
        frontier = []
        curr_cell = starting_cell
        curr_cell.visited = 1
        next_cell = None
        for neighbor in self.unvisited_neighbours(curr_cell):
            frontier.append((neighbor, curr_cell))
        while frontier:
            next_cell, curr_cell = random.choice(frontier)
            frontier.remove((next_cell, curr_cell))
            if not next_cell.visited:
                curr_cell.break_wall(next_cell)
            next_cell.visited = 1
            curr_cell = next_cell
            for neighbor in self.unvisited_neighbours(curr_cell):
                frontier.append((neighbor, next_cell))
            self.print_maze()
    
    def print_hexa_maze(self, filename=None):
        lines = []
        for r in self.grid:
            line = ""
            for c in r:
                line += format(c.hexa, "X")
            lines.append(line)
            if filename:
                with open(filename, "w") as f:
                    f.write("\n".join(lines))
            else:
                print(line)


""" def selection_function(cols, rows):
    m = Maze(cols, rows)
    center_col = cols // 2
    center_row = rows // 2
    
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
        "║\033[35m► 1) Generate Maze with backtracking\033[0m                                                   ║\n"
        "║\033[35m► 2) Generate Maze with prim\033[0m                                                           ║\n"
        "║                                                                                       ║\n"
        "║                                                                                       ║\n"
        "║                                                                                       ║\n"
        "║                                                                                       ║\n"
        "║                                                                                       ║\n"
        "╚═══════════════════════════════════════════════════════════════════════════════════════╝"
    ))
    print("\033[2J\033[H", end="")
    m = Maze(cols, rows)
    center_col = cols // 2
    center_row = rows // 2
    m.draw_42(center_col, center_row)
    match select:
        case 1:
            m.animated_backtracking(m.grid[0][0])
        case 2:
            m.prim_algoritm(m.grid[0][0])
    m.print_maze()
    m.print_hexa_maze("hexa.txt")

selection_function(11, 11) """


def selection_function(cols, rows):
    m = Maze(cols, rows)
    center_col = cols // 2
    center_row = rows // 2
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

        print("\033[2J\033[H", end="")
    m = Maze(cols, rows)
    center_col = cols // 2
    center_row = rows // 2
    m.draw_42(center_col, center_row)
    match select:
        case 1:
            m.animated_backtracking(m.grid[0][0])
        case 2:
            m.prim_algoritm(m.grid[0][0])
    m.print_maze()
    m.print_hexa_maze("hexa.txt")

selection_function(11, 11)
