from src.maze import Maze
from src.print_promt import flush

def selection_function() -> None:
    flush()
    args = {
        'HEIGHT': 20,
        'WIDTH': 20,
        'ENTRY': (0, 0),
        'EXIT': (19, 19),
        'PERFECT': True,
        'MAZE_ANIMATION': False,
        'RES_ANIMATINON': False,
        'RANDOM_42': False,
        'SEED': None,
        'ALGORITHM': 'dfs',
    }
    """ seed = args['SEED']
    if seed is None:
        seed = random.randint(0, 10**9)
        print(f"Generated seed: {seed}")
    random.seed(seed) """
    """ random_42 = args['RANDOM_42'] """
    cols, rows = args['WIDTH'], args['HEIGHT']
    start = args['ENTRY']
    end = args['EXIT']
    m = Maze(cols, rows, start, end)
    """ start_row, start_col = m.start
    end_row, end_col = m.end
    m.grid[start_row][start_col].start = True
    m.grid[end_row][end_col].end = True """
    """ if random_42 is True:
        m.random_draw_42(cols, rows)
    else:
        m.draw_42(cols, rows) """
    m.iterative_division(m.grid[0][0], args['MAZE_ANIMATION'], args['PERFECT'])
    """ m.bfs(args['RES_ANIMATINON']) """
    m.print_maze()
    m.print_hexa_maze("hexa.txt")


selection_function()
