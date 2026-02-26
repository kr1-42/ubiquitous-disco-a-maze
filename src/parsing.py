

from .check_config_cases import check_entry, check_exit, check_height, check_width
from sys import argv, stderr


def parse_input_file(input_file: str) -> dict | None:
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
    return ret


def check_parsed(parsed: dict) -> list | str:
    ret = []
    cases = {
            'WIDTH': check_width,
            'HEIGHT': check_height,
            'ENTRY': check_entry,
            'EXIT': check_exit
            }
    for key in parsed:
        checker = cases.get(key)
        pre_ret_check = checker(parsed[key], ret) if checker else None
        if isinstance(pre_ret_check, str):
            return pre_ret_check
        if pre_ret_check is not None:
            ret.append(pre_ret_check)
    return ret


def parse_args():
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
    for arg in ret:
        print(arg)
    return ret
