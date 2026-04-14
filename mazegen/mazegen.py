from .parsing import check_parsed
from .selection import selection_function


class MazeGenerator():
    def __init__(self, width: int = 20,
                 height: int = 20,
                 entry: tuple[int, int] = (0, 0),
                 exit: tuple[int, int] = (19, 19),
                 output_file: str = "maze.txt",
                 perfect: bool = True,
                 seed: int = 42,
                 algorithm: str = "back",
                 maze_animation: bool = False,
                 path_animation: bool = False,
                 random_42: bool = False,
                 color: str = "default",
                 animation_speed: float = 0.1) -> None:
        maze_conf = {
            'WIDTH': str(width),
            'HEIGHT': str(height),
            'ENTRY': str(entry).strip('()'),
            'EXIT': str(exit).strip('()'),
            'OUTPUT_FILE': output_file,
            'PERFECT': str(perfect).lower(),
            'SEED': str(seed),
            'ALGORITHM': algorithm,
            'MAZE_ANIMATION': str(maze_animation).lower(),
            'RES_ANIMATINON': str(path_animation).lower(),
            'RANDOM_42': str(random_42).lower(),
            'COLOR': color,
            'ANIMATION_SPEED': str(animation_speed)
        }
        parsed = check_parsed(maze_conf)
        if isinstance(parsed, str):
            raise ValueError(parsed)
        self.arg = parsed

    def generate(self) -> None:
        selection_function(self.arg, False)
