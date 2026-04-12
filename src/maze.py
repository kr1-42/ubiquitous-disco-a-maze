from .cell import Cell
from time import sleep
from typing import Optional
import random
from .maze_color import THEMES
from io import TextIOWrapper


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
        self.anim_speed = 0.5

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

    def unvisited_without_wall(self, cell: Optional["Cell"]) -> list["Cell"]:
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

    def visited_without_wall(self, cell: Optional["Cell"]) -> list["Cell"]:
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

    def if_is_3x3(self, r: int, c: int) -> bool:
        for dr, dc in [(-1, -1), (-1, 0), (0, -1), (0, 0)]:
            r0, c0 = r + dr, c + dc
            if 0 <= r0 < self.rows - 1 and 0 <= c0 < self.cols - 1:
                c1 = self.grid[r0][c0]
                c2 = self.grid[r0][c0+1]
                c3 = self.grid[r0+1][c0]
                c4 = self.grid[r0+1][c0+1]
                if not c1.south and not c1.east and \
                not c2.south and not c2.west and \
                not c3.north and not c3.east and \
                not c4.north and not c4.west:
                    return True
        return False

    def break_random_walls(self, count: int = 1) -> None:
        all_cells = [
        self.grid[r][c]
        for r in range(self.rows)
        for c in range(self.cols)
        if not self.grid[r][c].cell_42
        ]
        broken_successfully = 0
        while broken_successfully < count:
            cell = random.choice(all_cells)
            neighbors = []
            r, c = cell.row, cell.col
            if cell.north and r > 0 and not self.grid[r - 1][c].cell_42:
                neighbors.append(self.grid[r - 1][c])
            if cell.south and r < self.rows - 1 and not self.grid[r + 1][c].cell_42:
                neighbors.append(self.grid[r + 1][c])
            if cell.east and c < self.cols - 1 and not self.grid[r][c + 1].cell_42:
                neighbors.append(self.grid[r][c + 1])
            if cell.west and c > 0 and not self.grid[r][c - 1].cell_42:
                neighbors.append(self.grid[r][c - 1])
            if neighbors:
                neighbor = random.choice(neighbors)
                cell.break_wall(neighbor)
                if cell.hexa == 0 or neighbor.hexa == 0 or \
                self.if_is_3x3(cell.row, cell.col) or \
                self.if_is_3x3(neighbor.row, neighbor.col):
                    cell.create_wall(neighbor)
                else:
                    broken_successfully += 1

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
        sleep(self.anim_speed)

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
                    direction.visited = True
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
                      color: str = "default") -> None:
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
                    next_cell.visited = True
                curr_cell = next_cell
                for neighbor in self.unvisited_neighbours(curr_cell):
                    frontier.append((neighbor, next_cell))
                if animation:
                    self.print_maze(color=color)

    def break_all_walls(self) -> None:
        for r in range(self.rows):
            for c in range(self.cols):
                cell = self.grid[r][c]
                cell.visited = False
                cell.footsteps = 0
                cell.path = False
                cell.north = True if r == 0 else False
                cell.south = True if r == self.rows - 1 else False
                cell.west = True if c == 0 else False
                cell.east = True if c == self.cols - 1 else False
            cell.assign_hexa()

    def iterative_division(self,
                      animation: float = False,
                      color: str = "default") -> None:
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
                self.print_maze(color=color)


    def print_hexa_maze(self, file: TextIOWrapper | str) -> None:
        path_string = ""
        if self.start and self.end:
            curr_row, curr_col = self.start
            curr_cell = self.grid[curr_row][curr_col]
            while not (curr_row == self.end[0] and curr_col == self.end[1]):
                found = False
                for n in self.visited_without_wall(curr_cell):
                    if n.footsteps == curr_cell.footsteps - 1:
                        if n.row < curr_row: path_string += "N"
                        elif n.row > curr_row: path_string += "S"
                        elif n.col > curr_col: path_string += "E"
                        elif n.col < curr_col: path_string += "W"

                        curr_cell = n
                        curr_row, curr_col = n.row, n.col
                        found = True
                        break
                if not found: break
        def _write_hexa(target: TextIOWrapper) -> None:
            for row in self.grid:
                line = "".join(format(cell.hexa, "X") for cell in row)
                target.write(line + "\n")
            target.write("\n")
            target.write(f"{self.start[1]},{self.start[0]}\n")
            target.write(f"{self.end[1]},{self.end[0]}\n")
            target.write(path_string + "\n")

        try:
            if isinstance(file, str):
                with open(file, "w") as f:
                    _write_hexa(f)
            elif isinstance(file, TextIOWrapper):
                file.seek(0)
                file.truncate()
                _write_hexa(file)
                file.flush()
            else:
                raise ValueError("OUTPUT must be a file path or writable file object")
        except Exception as e:
            print(f"Errore durante il salvataggio: {e}")

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
