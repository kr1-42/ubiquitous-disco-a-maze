"""Cell class representing a single grid position in a maze.

This module defines the Cell class which represents a grid cell in a maze grid,
tracking wall positions and metadata for maze generation and pathfinding algorithms.
"""


class Cell:
    """Represents a single cell in the maze grid.
    
    A cell can have walls on each side (north, south, east, west) and
    tracks its position, visited status, and metadata for maze algorithms.
    
    Attributes:
        row: Row position in maze grid.
        col: Column position in maze grid.
        visited: Whether cell has been visited during generation.
        north: Wall existence on north side.
        south: Wall existence on south side.
        east: Wall existence on east side.
        west: Wall existence on west side.
        hexa: Hexadecimal encoding of wall configuration.
        cell_42: Whether cell is part of 42 logo pattern.
        path: Whether cell is part of solution path.
        footsteps: Distance from start in pathfinding.
        start: Whether this is the maze start cell.
        end: Whether this is the maze exit cell.
    """
    def __init__(self, row: int, col: int) -> None:
        """Initialize a cell with given row and column position.
        
        Args:
            row: Row coordinate in maze grid.
            col: Column coordinate in maze grid.
        """
        self.row: int = row
        self.col = col
        self.visited = False
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.hexa = 15
        self.cell_42 = False
        self.path = False
        self.footsteps = 0
        self.start = False
        self.end = False
        self.assign_hexa()

    def break_wall(self, next_cell: "Cell") -> None:
        """Remove the wall between this cell and another cell.
        
        Args:
            next_cell: Adjacent Cell object to remove wall with.
        
        Note:
            Automatically determines direction based on relative positions
            and updates hexadecimal encoding for both cells.
        """
        if self.row == next_cell.row:
            if self.col < next_cell.col:
                self.east = False
                next_cell.west = False
            else:
                self.west = False
                next_cell.east = False
        elif self.col == next_cell.col:
            if self.row < next_cell.row:
                self.south = False
                next_cell.north = False
            else:
                self.north = False
                next_cell.south = False
        self.assign_hexa()
        next_cell.assign_hexa()

    def create_wall(self, next_cell: "Cell") -> None:
        """Create a wall between this cell and another cell.
        
        Args:
            next_cell: Adjacent Cell object to create wall with.
        
        Note:
            Automatically determines direction based on relative positions
            and updates hexadecimal encoding for both cells.
        """
        if self.row == next_cell.row:
            if self.col < next_cell.col:
                self.east = True
                next_cell.west = True
            else:
                self.west = True
                next_cell.east = True
        elif self.col == next_cell.col:
            if self.row < next_cell.row:
                self.south = True
                next_cell.north = True
            else:
                self.north = True
                next_cell.south = True
        self.assign_hexa()
        next_cell.assign_hexa()

    def assign_hexa(self) -> None:
        """Calculate and assign hexadecimal representation for cell walls.
        
        Encodes wall configuration as hexadecimal value where:
        - bit 0 (1): north wall
        - bit 1 (2): east wall
        - bit 2 (4): south wall
        - bit 3 (8): west wall
        """
        self.hexa = 0
        if self.north:
            self.hexa |= 1
        if self.east:
            self.hexa |= 2
        if self.south:
            self.hexa |= 4
        if self.west:
            self.hexa |= 8

    def __repr__(self) -> str:
        """Return string representation of the cell.
        
        Returns:
            String showing cell position in format 'cell pos: (x, y)'.
        """
        return f"cell pos: ({self.col}, {self.row})"
