from .check_config_cases import check_entry, check_exit
from .check_config_cases import check_height, check_width
from .check_config_cases import get_output, get_perfect
from sys import argv, stderr
from typing import Any, Callable, TypedDict, cast


class MazeArgs(TypedDict):
    HEIGHT: int
    WIDTH: int
    ENTRY: tuple[int, int]
    EXIT: tuple[int, int]
    PERFECT: bool
    ALGORITHM: str
    MAZE_ANIMATION: bool
    RES_ANIMATINON: bool
    RANDOM_42: bool
    SEED: int | None
    COLOR: str


CheckerResult = int | bool | str | tuple[int, int] | object
Checker = Callable[[str, dict[str, Any]], CheckerResult]


def parse_input_file(input_file: str) -> dict[str, str] | None:
    with open(input_file, 'r') as f:
        lines = f.readlines()

    ret = {}
    for line in lines:
        line = line.strip()
        if line == '' or line.startswith('#'):
            continue
        dict_line = line.split('=')
        if len(dict_line) != 2:
            print(f"Invalid line: {line}")
            return None
        ret[dict_line[0].strip()] = dict_line[1].strip()
    f.close()
    return ret


def check_parsed(
        parsed: dict[str, str]
        ) -> MazeArgs | str:
    ret: dict[str, Any] = {
        'WIDTH': None,
        'HEIGHT': None,
        'ENTRY': None,
        'EXIT': None,
        'OUTPUT_FILE': None,
        'PERFECT': None,
        'SEED': None,
        'ALGORITHM': None,
        'MAZE_ANIMATION': False,
        'RES_ANIMATINON': False,
        'RANDOM_42': False,
        'COLOR': "default",
        'ANIMATION_SPEED': 1
    }
    cases = {
            'WIDTH': check_width,
            'HEIGHT': check_height,
            'ENTRY': check_entry,
            'EXIT': check_exit,
            'OUTPUT_FILE': get_output,
            'PERFECT': get_perfect,
            'SEED': (
                lambda value, _wh:
                int(value) if value.isdigit() else "SEED must be an integer"
            ),
            'ALGORITHM': (
                lambda value, _wh:
                value.lower() if value.lower() in ['back', 'prim', 'div']
                else "ALGORITHM must be either 'back', 'prim', or 'div'"
            )
            }
    for key in parsed:
        checker = cast(Checker | None, cases.get(key))
        pre_ret_check = checker(parsed[key], ret) if checker else None
        if key == 'ALGORITHM' and pre_ret_check is not None:
            ret[key] = pre_ret_check
            continue
        if isinstance(pre_ret_check, str):
            return pre_ret_check
        if pre_ret_check is not None:
            ret[key] = pre_ret_check
    return cast(MazeArgs, ret)

""" pattern = [
            "# # ###",
            "# #   #",
            "### ###",
            "  # #  ",
            "  # ###"
        ]
 center_col = cols // 2
        center_row = rows // 2
        start_row = center_row - 4 // 2
        start_col = center_col - 6 // 2 """
def check_ee_42(args: MazeArgs) -> None:
    center_col = args['WIDTH'] // 2
    center_row = args['HEIGHT'] // 2
    start_row = center_row - 4 // 2
    start_col = center_col - 6 // 2
    for i in range(4):
        for j in range(6):
            if (i == 0 or i == 3) and (j == 0 or j == 5):
                continue
            if args['ENTRY'][0] == start_col + j and args['ENTRY'][1] == start_row + i:
                raise ValueError("ENTRY cannot be on the position of the 42")
            if args['EXIT'][0] == start_col + j and args['EXIT'][1] == start_row + i:
                raise ValueError("EXIT cannot be on the position of the 42")

def parse_args() -> MazeArgs:
    if len(argv) != 2:
        print("Usage: python parsing.py <input_file>")
        exit(1)
    parsed = parse_input_file(argv[1])
    if parsed is None:
        print("Error: Invalid input file")
        exit(1)
    ret = check_parsed(parsed)
    if isinstance(ret, str):
        print(f"Error: {ret}", file=stderr)
        exit(1)
    try:
        if ret['RANDOM_42'] is False:
            check_ee_42(ret)
    except ValueError as e:
        print(f"Error: {e}", file=stderr)
        exit(1)
    return ret
