class Cell:
    def __init__(self, row, col):
        self.row: int = row
        self.col = col
        self.visited = False
        self.north = True
        self.south = True
        self.east = True
        self.west = True
        self.hexa = 15
        self._42 = False
        self.assign_hexa()
    
    def break_wall(self, next_cell):
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

    def assign_hexa(self):
        self.hexa = 0
        if self.north:
            self.hexa |= 1
        if self.south:
            self.hexa |= 2
        if self.east:
            self.hexa |= 4
        if self.west:
            self.hexa |= 8
