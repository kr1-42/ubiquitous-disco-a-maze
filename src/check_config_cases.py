
from io import TextIOWrapper


def check_width(value: str, _wh: list) -> int | str:
    try:
        width = int(value)
        if width <= 0:
            return "WIDTH must be a positive integer"
    except ValueError:
        return "WIDTH must be an integer"
    return width


def check_height(value: str, _wh: list) -> int | str:
    try:
        height = int(value)
        if height <= 0:
            return "HEIGHT must be a positive integer"
    except ValueError:
        return "HEIGHT must be an integer"
    return height


def check_entry(value: str, wh: dict) -> tuple | str:
    try:
        values = value.split(',')
        if len(values) != 2:
            return "ENTRY must be in the format 'x,y'"

        entryx = int(values[0])
        entryy = int(values[1])
        if entryx < 0 and entryy < 0:
            return "ENTRY must be a valid integer pair"
        if wh:
            if entryx >= wh['WIDTH'] or entryy >= wh['HEIGHT']:
                return "ENTRY must be within the bounds of WIDTH and HEIGHT"
    except ValueError:
        return "ENTRY must be an integer"
    return (entryx, entryy)


def check_exit(value: str, wh: dict) -> tuple | str:
    try:
        values = value.split(',')
        if len(values) != 2:
            return "EXIT must be in the format 'x,y'"

        exitx = int(values[0])
        exity = int(values[1])
        if exitx < 0 and exity < 0:
            return "EXIT must be a valid integer pair"
        if wh:
            if exitx == wh['ENTRY'][0] and exity == wh['ENTRY'][1]:
                return "EXIT cant be on the same position as ENTRY"
            if exitx >= wh['WIDTH'] or exity >= wh['HEIGHT']:
                return "EXIT must be within the bounds of WIDTH and HEIGHT"
    except ValueError:
        return "EXIT must be an integer"
    return (exitx, exity)


def get_output(value: str, _wh: list) -> str | TextIOWrapper:
    if value == '':
        return "OUTPUT must be a non-empty string"
    else:
        try:
            with open(value, 'w') as fd:
                return fd
        except Exception:
            return f"OUTPUT must be a valid file path: {value}"


def get_perfect(value: str, _wh: list) -> bool | str:
    if value.lower() == 'true':
        return True
    elif value.lower() == 'false':
        return False
    else:
        return "PERFECT must be either 'true' or 'false'"
