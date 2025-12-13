# src/matrix/maze.py
from collections import deque
from typing import Optional

def bfs_path(maze: list[list[int]], start: tuple[int,int], goal: tuple[int,int]) -> Optional[list[tuple[int,int]]]:
    rows, cols = len(maze), len(maze[0])
    def in_bounds(r,c): return 0 <= r < rows and 0 <= c < cols
    def open_cell(r,c): return maze[r][c] == 0
    q = deque([start])
    came = {start: None}
    for (r,c) in q:
        if (r,c) == goal:
            path = []
            while (r,c) is not None:
                path.append((r,c))
                prev = came[(r,c)]
                if prev is None: break
                r,c = prev
            return list(reversed(path))
        for dr,dc in [(1,0),(-1,0),(0,1),(0,-1)]:
            nr, nc = r+dr, c+dc
            if in_bounds(nr,nc) and open_cell(nr,nc) and (nr,nc) not in came:
                came[(nr,nc)] = (r,c)
                q.append((nr,nc))
    return None

def visualize(maze: list[list[int]], path: list[tuple[int,int]]|None) -> str:
    grid = [row[:] for row in maze]
    if path:
        for r,c in path: grid[r][c] = 2
    lines = []
    for r in range(len(grid)):
        row = "".join("#" if v==1 else "*" if v==2 else "." for v in grid[r])
        lines.append(row)
    return "\n".join(lines)