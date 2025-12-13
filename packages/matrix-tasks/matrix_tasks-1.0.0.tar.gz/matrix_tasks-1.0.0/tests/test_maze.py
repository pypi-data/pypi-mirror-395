# tests/test_maze.py
from src.matrix.maze import bfs_path
def test_bfs_path_found():
    maze = [
        [0,0,1],
        [1,0,0],
        [0,0,0],
    ]
    path = bfs_path(maze, (0,0), (2,2))
    assert path is not None
    assert path[0] == (0,0)
    assert path[-1] == (2,2)