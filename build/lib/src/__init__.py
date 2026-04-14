"""Package entry point for mazegen exports.

This module re-exports the public API for the maze generator package.

Classes:
    Maze: Represents a maze grid with cells, walls, entry, and exit positions.
        Use Maze when you need a concrete maze object for inspection, path
        validation, or custom rendering.

    Cell: Represents a single maze cell. It stores coordinates, wall state,
        visit state, and whether the cell has been carved. Use Cell when you
        need low-level access to maze geometry or custom cell-level logic.

    MazeGenerator: Builds and displays mazes.
        - Construct it with width, height, output format, and optional
          configuration values.
        - Call its generator method(s) to create the maze.
        - Print the maze object or its string representation to show the maze.

Validation helpers:
    check_entry(entry): Validate maze entry coordinates.
    check_exit(exit): Validate maze exit coordinates.
    check_height(height): Validate maze height input.
    check_width(width): Validate maze width input.
    get_output(output): Validate output format selection.
    get_perfect(perfect): Validate whether the maze should be perfect.
    check_parsed(parsed): Validate parsed configuration input.

Usage example:
    from mazegen import MazeGenerator

    generator = MazeGenerator(width=20, height=10, output='text')
    maze = generator.generate()
    print(maze)

in MzeGenerator you can pass any of the following keyword arguments:
    - width (int): The width of the maze
      (default: 20).
    - height (int): The height of the maze
      (default: 20).
    - entry (tuple[int, int]): The entry point coordinates
      (default: (0, 0)).
    - exit (tuple[int, int]): The exit point coordinates
      (default: (19, 19)).
    - output_file (str): The output file name for the maze
      (default: "maze.txt").
    - perfect (bool): Whether to generate a perfect maze
      (default: True).
    - seed (int): The random seed for maze generation
      (default: 42).
    - algorithm (str): The maze generation algorithm to use
      (default: "back").
    - maze_animation (bool): Whether to animate the maze generation
      (default: False).
    - path_animation (bool): Whether to animate the pathfinding
      (default: False).
    - random_42 (bool): Whether to use a random seed instead of 42
      (default: False).
    - color (str): The color scheme for maze display
      (default: "default").
    - animation_speed (float): The speed of animations in seconds
      (default: 0.1
If this package is installed from a wheel, import the published package name
and then instantiate `MazeGenerator` exactly as shown. The package is designed
so that `MazeGenerator` can be called with simple typed keyword arguments and
then printed to display the generated maze.
"""
from .check_config_cases import check_entry, check_exit
from .check_config_cases import check_height, check_width
from .check_config_cases import get_output, get_perfect
from .maze import Maze
from .cell import Cell
from .mazegen import MazeGenerator
from .parsing import check_parsed
__all__ = [
    'check_entry',
    'check_exit',
    'check_height',
    'check_width',
    'get_output',
    'get_perfect',
    'Maze',
    'Cell',
    'MazeGenerator',
    'check_parsed'
]
