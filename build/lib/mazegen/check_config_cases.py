
from __future__ import annotations

"""Configuration validation functions for maze parameters.

This module provides validators for maze configuration parameters including
width, height, entry/exit points, output files, and other settings.
"""
from io import TextIOWrapper
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .parsing import MazeArgs


def check_width(value: str, _wh: MazeArgs) -> int | str:
    """Validate and return width value.

    Args:
        value: String representation of width.
        _wh: Maze arguments dictionary (for context).

    Returns:
        Validated width as integer, or error message string.

    Raises:
        Does not raise exceptions; returns error strings instead.
    """
    try:
        width = int(value)
        if width <= 9 or width > 45:
            return "WIDTH must be a positive integer between 1 and 45"
    except ValueError:
        return "WIDTH must be an integer"
    return width


def check_height(value: str, wh: MazeArgs) -> int | str:
    """Validate and return height value.

    Args:
        value: String representation of height.
        wh: Maze arguments dictionary containing width for cross-validation.

    Returns:
        Validated height as integer, or error message string.
    """
    try:
        height = int(value)
        if height <= 7 or height > 45:
            return "HEIGHT must be a positive integer between 1 and 45"
        elif height < 7 and wh['WIDTH'] < 9:
            return "" \
                "HEIGHT and WIDTH must both be at " \
                "least 10 if one of them is less than 10"
    except ValueError:
        return "HEIGHT must be an integer"
    return height


def check_entry(value: str, wh: MazeArgs) -> tuple[int, int] | str:
    """Validate and return entry point coordinates.

    Args:
        value: String in format 'x,y' representing entry coordinates.
        wh: Maze arguments dictionary containing maze dimensions.

    Returns:
        Tuple of (x, y) coordinates as integers, or error message string.
    """
    try:
        values = value.split(',')
        if len(values) != 2:
            return "ENTRY must be in the format 'x,y'"
        entryx = int(values[0])
        entryy = int(values[1])
        if entryx < 0 or entryy < 0:
            return "ENTRY must be a valid integer pair"
        if entryx >= wh['WIDTH'] or entryy >= wh['HEIGHT']:
            return "ENTRY must be within the bounds of WIDTH and HEIGHT"
    except ValueError:
        return "ENTRY must be an integer"
    return (entryx, entryy)


def check_exit(value: str, wh: MazeArgs) -> tuple[int, int] | str:
    """Validate and return exit point coordinates.

    Args:
        value: String in format 'x,y' representing exit coordinates.
        wh: Maze arguments dictionary
            containing maze dimensions and entry point.

    Returns:
        Tuple of (x, y) coordinates as integers, or error message string.
    """
    try:
        values = value.split(',')
        if len(values) != 2:
            return "EXIT must be in the format 'x,y'"

        exitx = int(values[0])
        exity = int(values[1])
        if exitx < 0 or exity < 0:
            return "EXIT must be a valid integer pair"
        if wh:
            if exitx == wh['ENTRY'][0] and exity == wh['ENTRY'][1]:
                return "EXIT cant be on the same position as ENTRY"
            if exitx >= wh['WIDTH'] or exity >= wh['HEIGHT']:
                return "EXIT must be within the bounds of WIDTH and HEIGHT"
    except ValueError:
        return "EXIT must be an integer"
    return (exitx, exity)


def get_output(value: str, _wh: MazeArgs) -> str | TextIOWrapper:
    """Validate and open output file.

    Args:
        value: File path string for output.
        _wh: Maze arguments dictionary (for context).

    Returns:
        File object if path is valid, or error message string.
    """
    if value == '':
        return "OUTPUT must be a non-empty string"
    else:
        try:
            return open(value, 'w')
        except Exception:
            return f"OUTPUT must be a valid file path: {value}"


def get_perfect(value: str, _wh: MazeArgs) -> bool | str:
    """Validate and return perfect maze setting.

    Args:
        value: String value 'true' or 'false'.
        _wh: Maze arguments dictionary (for context).

    Returns:
        Boolean value if valid, or error message string.
    """
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        return "PERFECT must be either 'true' or 'false'"
