from cell import Cell
from time import sleep
import random


class Maze:
    def __init__(self, rows, cols, start, end):
        self.rows = rows
        self.cols = cols
        self.start = start
        self.end = end
        self.grid: list[list[Cell]] = [[Cell(r, c) for c in range(cols)] for r in range(rows)]

    def has_unvisited_cells(self) -> bool:
        for r in self.grid:
            for c in r:
                if not c.visited:
                    return True
        return False

    def set_all_unvisited(self):
        for r in self.grid:
            for c in r:
                c.visited = False

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

    def unvisited_without_wall(self, cell):
        unvisited = []
        if cell.row > 0 and not self.grid[cell.row - 1][cell.col].visited and not cell.north:
            unvisited.append(self.grid[cell.row - 1][cell.col])
        if cell.row < self.rows - 1 and not self.grid[cell.row + 1][cell.col].visited and not cell.south:
            unvisited.append(self.grid[cell.row + 1][cell.col])
        if cell.col < self.cols - 1 and not self.grid[cell.row][cell.col + 1].visited and not cell.east:
            unvisited.append(self.grid[cell.row][cell.col + 1])
        if cell.col > 0 and not self.grid[cell.row][cell.col - 1].visited and not cell.west:
            unvisited.append(self.grid[cell.row][cell.col - 1])
        return unvisited

    def visited_without_wall(self, cell):
        unvisited = []
        if cell.row > 0 and self.grid[cell.row - 1][cell.col].visited and not cell.north:
            unvisited.append(self.grid[cell.row - 1][cell.col])
        if cell.row < self.rows - 1 and self.grid[cell.row + 1][cell.col].visited and not cell.south:
            unvisited.append(self.grid[cell.row + 1][cell.col])
        if cell.col < self.cols - 1 and self.grid[cell.row][cell.col + 1].visited and not cell.east:
            unvisited.append(self.grid[cell.row][cell.col + 1])
        if cell.col > 0 and self.grid[cell.row][cell.col - 1].visited and not cell.west:
            unvisited.append(self.grid[cell.row][cell.col - 1])
        return unvisited

    def print_maze(self):
        print('\033[3J\033[H')
        wall = "\033[48;2;254;254;254m  \033[0m"
        path = "\033[48;2;0;0;0m  \033[0m"
        wall_42 = "\033[48;2;0;0;255m  \033[0m"
        path_42 = "\033[48;2;0;0;255m  \033[0m"
        path_solution = "\033[48;2;255;255;0m  \033[0m"
        start = "\033[48;2;0;255;0m  \033[0m"
        end = "\033[48;2;255;0;0m  \033[0m"
        print(wall * (self.cols * 2 + 1))
        for r in self.grid:
            line = wall
            bottom = wall
            for c in r:
                if c.start:
                    line += start
                    if c.east:
                        line += wall
                    else:
                        if self.grid[c.row][c.col + 1].path:
                            line += path_solution
                        else:
                            line += path
                    if c.south:
                        bottom += wall
                    else:
                        if self.grid[c.row + 1][c.col].path:
                            bottom += path_solution
                        else:
                            bottom += path
                elif c.end:
                    line += end
                    if c.east:
                        line += wall
                    else:
                        if self.grid[c.row][c.col + 1].path:
                            line += path_solution
                        else:
                            line += path
                    if c.south:
                        bottom += wall
                    else:
                        if self.grid[c.row + 1][c.col].path:
                            bottom += path_solution
                        else:
                            bottom += path
                elif c._42:
                    line += path_42
                    if c.east and c.col < self.cols - 1 and self.grid[c.row][c.col + 1]._42:
                        line += wall_42
                    else:
                        line += wall
                    if c.south and c.row < self.rows - 1 and self.grid[c.row + 1][c.col]._42:
                        bottom += wall_42
                    else:
                        bottom += wall
                elif c.path:
                    line += path_solution
                    if c.east:
                        line += wall
                    else:
                        if c.path and self.grid[c.row][c.col + 1].path:
                            line += path_solution
                        elif c.path and self.grid[c.row][c.col + 1].end:
                            line += path_solution
                        elif c.path and self.grid[c.row][c.col + 1].start:
                            line += path_solution
                        else:
                            line += path
                    if c.south:
                        bottom += wall
                    else:
                        if c.path and self.grid[c.row + 1][c.col].path:
                            bottom += path_solution
                        elif c.path and self.grid[c.row + 1][c.col].end:
                            bottom += path_solution
                        elif c.path and self.grid[c.row + 1][c.col].start:
                            bottom += path_solution
                        else:
                            bottom += path
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
        sleep(0.5)

    def draw_42(self, rows, cols):
        pattern = [
            "#   ###",
            "#     #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]
        center_col = cols // 2
        center_row = rows // 2
        start_row = center_row - 4 // 2
        start_col = center_col - 6 // 2
        for r, row in enumerate(pattern):
            for c, ch in enumerate(row):
                if ch == "#":
                    self.grid[start_row + r][start_col + c].visited = True
                    self.grid[start_row + r][start_col + c]._42 = True
    
    def random_draw_42(self, rows, cols):
        pattern = [
            "#   ###",
            "#     #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]
        avaliable_cols = cols - 8
        avaliable_rows = rows - 5
        while True:
            autorized = True
            draw_row = random.randint(0, avaliable_rows)
            draw_col = random.randint(1, avaliable_cols)
            for r, row in enumerate(pattern):
                for c, ch in enumerate(row):
                    if ch == "#" and (self.grid[draw_row + r][draw_col + c].start or self.grid[draw_row + r][draw_col + c].end):            
                        autorized = False
            if autorized:
                break
        for r, row in enumerate(pattern):
            for c, ch in enumerate(row):
                if ch == "#":
                    self.grid[draw_row + r][draw_col + c].visited = True
                    self.grid[draw_row + r][draw_col + c]._42 = True

    def backtracking(self, starting_cell=None, animation=False, bad=False):
        stack = []
        curr_cell = starting_cell
        curr_cell.visited = 1
        while self.has_unvisited_cells():
            unvisited = self.unvisited_neighbours(curr_cell)
            if unvisited:
                direction = random.choice(unvisited)
                curr_cell.break_wall(direction)
                if bad:
                    direction.visited = random.randint(0, 100) < 80
                else:
                    direction.visited = 1
                if self.unvisited_neighbours(curr_cell):
                    stack.append(curr_cell)
                curr_cell = direction
            else:
                curr_cell = stack.pop()
            if animation:
                self.print_maze()

    def prim_algoritm(self, starting_cell=None, animation=False, bad=False):
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
            if bad:
                next_cell.visited = random.randint(0, 100) < 99
            else:
                next_cell.visited = 1
            curr_cell = next_cell
            for neighbor in self.unvisited_neighbours(curr_cell):
                frontier.append((neighbor, next_cell))
            if animation:
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

    def bfs(self, animation=False):
        self.set_all_unvisited()
        stack = []
        neighbours: list[Cell] = []
        start_row, start_col = self.start
        end_row, end_col = self.end
        self.grid[start_row][start_col].start = True
        self.grid[end_row][end_col].end = True
        curr_cell = self.grid[end_row][end_col]
        curr_cell.visited = 1
        stack.append(curr_cell)
        while self.has_unvisited_cells():
            curr_cell = stack.pop(0)
            if curr_cell.start:
                break
            neighbours = self.unvisited_without_wall(curr_cell)
            for n in neighbours:
                n.footsteps += curr_cell.footsteps + 1
                n.visited = 1
                stack.append(n)
        while not curr_cell.end:
            neighbours = self.visited_without_wall(curr_cell)
            for n in neighbours:
                if n.footsteps == curr_cell.footsteps - 1:
                    curr_cell = n
                    curr_cell.path = 1
                    if animation:
                        self.print_maze()
                    break

