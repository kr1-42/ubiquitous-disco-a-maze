from src.maze import Maze
from src.print_promt import flush

def selection_function() -> None:
    flush()
    args = {'HEIGHT': 24,
            'WIDTH': 24,
            'ENTRY': (0, 0),
            'EXIT': (20, 20),
            'MAZE_ANIMATION': False,
            'PATH_ANIMATION': False,
            'PERFECT': True,
            'RANDOM_42': False}
    random_42 = args['RANDOM_42']
    cols, rows = args['HEIGHT'], args['WIDTH']
    start = args['ENTRY']
    end = args['EXIT']
    m = Maze(cols, rows, start, end)
    start_row, start_col = m.start
    end_row, end_col = m.end
    m.grid[start_row][start_col].start = True
    m.grid[end_row][end_col].end = True
    if random_42 is True:
        m.random_draw_42(cols, rows)
    else:
        m.draw_42(cols, rows)
    m.backtracking(m.grid[0][0], args['MAZE_ANIMATION'], args['PERFECT'])
    m.bfs(args['PATH_ANIMATION'])
    m.print_maze()
    m.print_hexa_maze("hexa.txt")

selection_function()