from .cell import Cell
from time import sleep
from typing import Optional
import random
from .maze_color import THEMES


class Maze:
    def __init__(self,
                 rows: int,
                 cols: int,
                 start: tuple[int, int],
                 end: tuple[int, int]) -> None:
        self.rows = rows
        self.cols = cols
        self.start = start
        self.end = end
        self.grid: list[list[Cell]] = [
            [Cell(r, c) for c in range(cols)]
            for r in range(rows)]
        self.colors = THEMES['default']

    def has_unvisited_cells(self) -> bool:
        for r in self.grid:
            for c in r:
                if not c.visited:
                    return True
        return False

    def set_all_unvisited(self) -> None:
        for r in self.grid:
            for c in r:
                c.visited = False

    def unvisited_neighbours(self, cell: "Cell") -> list[Cell]:
        unvisited = []
        if (cell.row > 0
                and not self.grid[cell.row - 1][cell.col].visited):
            unvisited.append(self.grid[cell.row - 1][cell.col])
        if (cell.row < self.rows - 1
                and not self.grid[cell.row + 1][cell.col].visited):
            unvisited.append(self.grid[cell.row + 1][cell.col])
        if (cell.col < self.cols - 1
                and not self.grid[cell.row][cell.col + 1].visited):
            unvisited.append(self.grid[cell.row][cell.col + 1])
        if (cell.col > 0
                and not self.grid[cell.row][cell.col - 1].visited):
            unvisited.append(self.grid[cell.row][cell.col - 1])
        return unvisited

    def unvisited_without_wall(self, cell: Optional["Cell"]) -> list:
        unvisited = []
        if cell:
            if (cell.row > 0
                    and not self.grid[cell.row - 1][cell.col].visited
                    and not cell.north):
                unvisited.append(self.grid[cell.row - 1][cell.col])
            if (cell.row < self.rows - 1
                    and not self.grid[cell.row + 1][cell.col].visited
                    and not cell.south):
                unvisited.append(self.grid[cell.row + 1][cell.col])
            if (cell.col < self.cols - 1
                    and not self.grid[cell.row][cell.col + 1].visited
                    and not cell.east):
                unvisited.append(self.grid[cell.row][cell.col + 1])
            if (cell.col > 0
                    and not self.grid[cell.row][cell.col - 1].visited
                    and not cell.west):
                unvisited.append(self.grid[cell.row][cell.col - 1])
        return unvisited

    def visited_without_wall(self, cell: Optional["Cell"]) -> list:
        unvisited = []
        if cell:
            if (cell.row > 0
                    and self.grid[cell.row - 1][cell.col].visited
                    and not cell.north):
                unvisited.append(self.grid[cell.row - 1][cell.col])
            if (cell.row < self.rows - 1
                    and self.grid[cell.row + 1][cell.col].visited
                    and not cell.south):
                unvisited.append(self.grid[cell.row + 1][cell.col])
            if (cell.col < self.cols - 1
                    and self.grid[cell.row][cell.col + 1].visited
                    and not cell.east):
                unvisited.append(self.grid[cell.row][cell.col + 1])
            if (cell.col > 0
                    and self.grid[cell.row][cell.col - 1].visited
                    and not cell.west):
                unvisited.append(self.grid[cell.row][cell.col - 1])
        return unvisited

    def remove_diagonal_wall(self, curr_cell: Cell) -> bool:
        if curr_cell:
            if curr_cell.row + 1 < self.rows and curr_cell.col + 1 < self.cols:
                diagonal_cell = self.grid[curr_cell.row + 1][curr_cell.col + 1]
                se = not curr_cell.east and not curr_cell.south
                nw = not diagonal_cell.west and not diagonal_cell.north
                return se and nw
        return False

    def print_maze(self, color: str = "default") -> None:
        print('\033[3J\033[H')
        self.colors = THEMES[color]
        print(self.colors['wall'] * (self.cols * 2 + 1))
        for r in self.grid:
            line = self.colors['wall']
            bottom = self.colors['wall']
            for c in r:
                if c.start:
                    line += self.colors['start']
                    if c.east:
                        line += self.colors['wall']
                    else:
                        if self.grid[c.row][c.col + 1].path:
                            line += self.colors['path_solution']
                        else:
                            line += self.colors['path']
                    if c.south:
                        bottom += self.colors['wall']
                    else:
                        if self.grid[c.row + 1][c.col].path:
                            bottom += self.colors['path_solution']
                        else:
                            bottom += self.colors['path']
                elif c.end:
                    line += self.colors['end']
                    if c.east:
                        line += self.colors['wall']
                    else:
                        if self.grid[c.row][c.col + 1].path:
                            line += self.colors['path_solution']
                        else:
                            line += self.colors['path']
                    if c.south:
                        bottom += self.colors['wall']
                    else:
                        if self.grid[c.row + 1][c.col].path:
                            bottom += self.colors['path_solution']
                        else:
                            bottom += self.colors['path']
                elif c.cell_42:
                    line += self.colors['wall_42']
                    if (c.east
                            and c.col < self.cols - 1
                            and self.grid[c.row][c.col + 1].cell_42):
                        line += self.colors['wall_42']
                    else:
                        line += self.colors['wall']
                    if (c.south
                            and c.row < self.rows - 1
                            and self.grid[c.row + 1][c.col].cell_42):
                        bottom += self.colors['wall_42']
                    else:
                        bottom += self.colors['wall']
                elif c.path:
                    line += self.colors['path_solution']
                    if c.east:
                        line += self.colors['wall']
                    else:
                        if c.path and self.grid[c.row][c.col + 1].path:
                            line += self.colors['path_solution']
                        elif c.path and self.grid[c.row][c.col + 1].end:
                            line += self.colors['path_solution']
                        elif c.path and self.grid[c.row][c.col + 1].start:
                            line += self.colors['path_solution']
                        else:
                            line += self.colors['path']
                    if c.south:
                        bottom += self.colors['wall']
                    else:
                        if c.path and self.grid[c.row + 1][c.col].path:
                            bottom += self.colors['path_solution']
                        elif c.path and self.grid[c.row + 1][c.col].end:
                            bottom += self.colors['path_solution']
                        elif c.path and self.grid[c.row + 1][c.col].start:
                            bottom += self.colors['path_solution']
                        else:
                            bottom += self.colors['path']
                else:
                    line += self.colors['path']
                    if c.east:
                        line += self.colors['wall']
                    else:
                        line += self.colors['path']
                    if c.south:
                        bottom += self.colors['wall']
                    else:
                        bottom += self.colors['path']
                if self.remove_diagonal_wall(self.grid[c.row][c.col]):
                    bottom += self.colors['path']
                else:
                    bottom += self.colors['wall']
            print(line)
            print(bottom)
        sleep(0.0005)

    def draw_42(self, rows: int, cols: int) -> None:
        pattern = [
            "# # ###",
            "# #   #",
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
                    self.grid[start_row + r][start_col + c].cell_42 = True

    def random_draw_42(self, rows: int, cols: int) -> None:
        pattern = [
            "# # ###",
            "# #   #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]
        avaliable_cols = cols - 8
        avaliable_rows = rows - 5
        while True:
            autorized = True
            draw_row = random.randint(1, avaliable_rows)
            draw_col = random.randint(1, avaliable_cols)
            for r, row in enumerate(pattern):
                for c, ch in enumerate(row):
                    if (ch == "#"
                        and (self.grid[draw_row + r][draw_col + c].start
                             or self.grid[draw_row + r][draw_col + c].end)):
                        autorized = False
            if autorized:
                break
        for r, row in enumerate(pattern):
            for c, ch in enumerate(row):
                if ch == "#":
                    self.grid[draw_row + r][draw_col + c].visited = True
                    self.grid[draw_row + r][draw_col + c].cell_42 = True

    def backtracking(self,
                     starting_cell: Optional["Cell"] = None,
                     animation: bool = False,
                     perfect: bool = True,
                     color: str = "default") -> None:
        stack = []
        curr_cell = None
        if starting_cell:
            curr_cell = starting_cell
        if curr_cell:
            curr_cell.visited = True
        while self.has_unvisited_cells():
            if curr_cell:
                unvisited = self.unvisited_neighbours(curr_cell)
            if unvisited:
                direction = random.choice(unvisited)
                if curr_cell:
                    curr_cell.break_wall(direction)
                if perfect:
                    direction.visited = True
                else:
                    direction.visited = random.randint(0, 100) < 80
                if curr_cell and self.unvisited_neighbours(curr_cell):
                    stack.append(curr_cell)
                curr_cell = direction
            else:
                curr_cell = stack.pop()
            if animation:
                self.print_maze(color=color)

    def prim_algoritm(self,
                      starting_cell: Optional["Cell"] = None,
                      animation: float = False,
                      perfect: float = True) -> None:
        frontier = []
        if starting_cell:
            curr_cell = starting_cell
            curr_cell.visited = True
            next_cell = None
            for neighbor in self.unvisited_neighbours(curr_cell):
                frontier.append((neighbor, curr_cell))
            while frontier:
                next_cell, curr_cell = random.choice(frontier)
                frontier.remove((next_cell, curr_cell))
                if not next_cell.visited:
                    curr_cell.break_wall(next_cell)
                if perfect:
                    next_cell.visited = True
                else:
                    next_cell.visited = random.randint(0, 100) < 99
                curr_cell = next_cell
                for neighbor in self.unvisited_neighbours(curr_cell):
                    frontier.append((neighbor, next_cell))
                if animation:
                    self.print_maze()

    def break_all_walls(self) -> None:
        for r in self.grid:
            for c in r:
                if self.grid[c.row][c.col].cell_42 is False:
                    self.grid[c.row][c.col].north = False
                    self.grid[c.row][c.col].west = False
                    if c.col != self.cols - 1:
                        self.grid[c.row][c.col].east = False
                    if c.row != self.rows - 1:
                        self.grid[c.row][c.col].south = False

    def iterative_division(self,
                      starting_cell: Optional["Cell"] = None,
                      animation: float = False,
                      perfect: float = True) -> None:
        self.break_all_walls()
        stack = []
        stack.append(((0, 0), (self.rows - 1, self.cols - 1)))
        while stack:
            curr_area = stack.pop()
            y1, x1 = curr_area[0]
            y2, x2 = curr_area[1]
            width = x2 - x1
            height = y2 - y1
            if width < 1 or height < 1:
                continue
            if width > height:
                if width >= 1:
                    wall_x = random.randrange(x1, x2)
                    hole_y = random.randrange(y1, y2 + 1)
                    for y in range(y1, y2 + 1):
                        self.grid[y][wall_x].create_wall(
                            self.grid[y][wall_x + 1]
                        )
                    self.grid[hole_y][wall_x].break_wall(
                        self.grid[hole_y][wall_x + 1]
                    )
                    stack.append(((y1, x1), (y2, wall_x)))
                    stack.append(((y1, wall_x + 1), (y2, x2)))
            else:
                if height >= 1:
                    wall_y = random.randrange(y1, y2)
                    hole_x = random.randrange(x1, x2 + 1)
                    for x in range(x1, x2 + 1):
                        self.grid[wall_y][x].create_wall(
                            self.grid[wall_y + 1][x]
                        )
                    self.grid[wall_y][hole_x].break_wall(
                        self.grid[wall_y + 1][hole_x]
                    )
                    stack.append(((y1, x1), (wall_y, x2)))
                    stack.append(((wall_y + 1, x1), (y2, x2)))
            if animation:
                self.print_maze()

    def print_hexa_maze(self, filename: Optional[str] = None) -> None:
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

    def bfs(self, animation: bool = False, color: str = "default") -> None:
        self.set_all_unvisited()
        stack = []
        neighbours: list[Cell] = []
        start_row: int = 0
        start_col: int = 0
        end_row: int = 0
        end_col: int = 0
        if self.start:
            start_row, start_col = self.start
        if self.end:
            end_row, end_col = self.end
        self.grid[start_row][start_col].start = True
        self.grid[end_row][end_col].end = True
        curr_cell = self.grid[end_row][end_col]
        curr_cell.visited = True
        stack.append(curr_cell)
        while self.has_unvisited_cells():
            curr_cell = stack.pop(0)
            if curr_cell.start:
                break
            neighbours = self.unvisited_without_wall(curr_cell)
            for n in neighbours:
                n.footsteps += curr_cell.footsteps + 1
                n.visited = True
                stack.append(n)
        while not curr_cell.end:
            neighbours = self.visited_without_wall(curr_cell)
            for n in neighbours:
                if n.footsteps == curr_cell.footsteps - 1:
                    curr_cell = n
                    curr_cell.path = True
                    if animation:
                        self.print_maze(color=color)
                    break
