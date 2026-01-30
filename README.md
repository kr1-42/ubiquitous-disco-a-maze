# a-maze - Maze Generator Project

A Python maze generation project with a reusable `mazegen` package.

## Project Structure

```
a-maze/
├── pyproject.toml          # Package build configuration
├── src/
│   └── mazegen/            # Reusable maze generator package
│       ├── __init__.py
│       └── maze_generator.py
├── a_maze_ing.py           # Main executable
├── output_validator.py     # Maze output validator
└── configs/                # Configuration files
```

---

# mazegen - Reusable Maze Generation Library

A standalone Python module for generating random mazes using multiple algorithms.

## Installation

### From Package (pip)

```bash
# Install from wheel
pip install mazegen-1.0.0-py3-none-any.whl

# Or install from source distribution
pip install mazegen-1.0.0.tar.gz
```

### From Source (Development)

```bash
pip install -e .
```

## Quick Start

### Basic Usage

```python
from mazegen import MazeGenerator

# Create a generator with default parameters (10x10 maze)
gen = MazeGenerator()
gen.generate()
gen.print_maze()
```

### Custom Parameters

```python
from mazegen import MazeGenerator

# Create a 20x15 maze with a specific seed for reproducibility
gen = MazeGenerator(width=20, height=15, seed=12345)
gen.generate()

# Use different algorithms: 'backtracking', 'kruskal', or 'prim'
gen = MazeGenerator(width=10, height=10, algorithm='kruskal')
gen.generate()
```

### Accessing the Maze Structure

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=5, height=5, seed=42)
gen.generate()

# Get the internal structure (2D grid)
structure = gen.get_structure()

# Each cell contains wall information
cell = structure[0][0]  # Top-left cell (y=0, x=0)
print(cell['walls'])    # {'N': True, 'E': False, 'S': True, 'W': True}
# True = wall present, False = passage open

# Access specific wall
has_north_wall = structure[0][0]['walls']['N']
```

### Finding a Solution

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=10, height=10, seed=42)
gen.generate()

# Solve from default start (0,0) to end (width-1, height-1)
solution = gen.solve()
print(f"Solution has {len(solution)} steps")
print(f"Path: {solution}")  # List of (x, y) coordinates

# Solve with custom start/end
path = gen.solve(start=(0, 0), end=(5, 5))

# Visualize the solution
gen.print_maze(show_solution=True)
```

### Export Formats

```python
from mazegen import MazeGenerator

gen = MazeGenerator(width=10, height=10, seed=42)
gen.generate()

# Get hexadecimal string (compatible with output_validator.py)
hex_output = gen.to_hex_string()
print(hex_output)

# Save to file
gen.save_to_file("maze_output.txt")
```

### Convenience Function

```python
from mazegen import generate_maze

# Generate a maze in one line
maze = generate_maze(15, 15, seed=42, algorithm='prim')
maze.print_maze()
```

## API Reference

### MazeGenerator Class

#### Constructor

```python
MazeGenerator(
    width: int = 10,      # Maze width in cells (>= 2)
    height: int = 10,     # Maze height in cells (>= 2)
    seed: int = None,     # Random seed for reproducibility
    algorithm: str = 'backtracking'  # 'backtracking', 'kruskal', or 'prim'
)
```

#### Methods

| Method | Description |
|--------|-------------|
| `generate()` | Generate the maze. Returns self for chaining. |
| `solve(start, end)` | Find shortest path. Returns list of (x, y) coordinates. |
| `get_structure()` | Get the internal 2D grid structure. |
| `get_solution()` | Get the last computed solution path. |
| `to_hex_string()` | Convert maze to hexadecimal format. |
| `save_to_file(path)` | Save maze to file in hex format. |
| `print_maze(show_solution)` | Print ASCII visualization. |

### Maze Structure Format

The internal structure is a 2D list `grid[y][x]` where each cell is:
```python
{
    'walls': {
        'N': bool,  # True = wall present (North)
        'E': bool,  # True = wall present (East)
        'S': bool,  # True = wall present (South)
        'W': bool   # True = wall present (West)
    },
    'visited': bool  # Internal use
}
```

### Hexadecimal Output Format

Each cell is encoded as a single hex digit (0-F):
- Bit 0 (1): North passage **open**
- Bit 1 (2): East passage **open**
- Bit 2 (4): South passage **open**
- Bit 3 (8): West passage **open**

Example: `6` = `0110` binary = East and South passages open

## Building the Package

### Requirements

```bash
pip install build
```

### Build Commands

```bash
# Build both wheel and source distribution
python -m build

# Output files will be in dist/
# - mazegen-1.0.0-py3-none-any.whl
# - mazegen-1.0.0.tar.gz
```

### Build in a Virtual Environment

```bash
# Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or: venv\Scripts\activate  # Windows

# Install build tools
pip install build

# Build the package
python -m build

# The package files will be in dist/
ls dist/
```

## Algorithms

### Recursive Backtracking (default)
- Uses depth-first search with backtracking
- Creates long, winding passages
- Guaranteed to produce a perfect maze (one solution)

### Kruskal's Algorithm
- Randomized version of Kruskal's minimum spanning tree
- Creates more uniform distribution of passages
- Uses union-find data structure

### Prim's Algorithm
- Randomized version of Prim's minimum spanning tree
- Tends to create mazes with shorter dead-ends
- Grows from a single starting point

## License

MIT License
