def path_blocked(grid, path):
    for node in path:
        if grid.grid[node[0]][node[1]] == 2:
            return True
    return False
