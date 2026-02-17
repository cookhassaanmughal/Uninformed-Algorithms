import random
from constants import *

class Grid:
    def __init__(self):
        self.rows = ROWS
        self.cols = COLS
        self.grid = [[0 for _ in range(self.cols)] for _ in range(self.rows)]

        self.start = (0, 0)
        self.target = (10, 16)

        self.grid[self.start[0]][self.start[1]] = "S"
        self.grid[self.target[0]][self.target[1]] = "T"

        self.generate_static_walls()

    def generate_static_walls(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if random.random() < 0.15 and (r, c) not in [self.start, self.target]:
                    self.grid[r][c] = 1  # wall

    def is_valid(self, pos):
        r, c = pos
        return (0 <= r < self.rows and
                0 <= c < self.cols and
                self.grid[r][c] != 1)

    def spawn_dynamic_obstacle(self):
        import random
        if random.random() < DYNAMIC_PROBABILITY:
            r = random.randint(0, self.rows - 1)
            c = random.randint(0, self.cols - 1)
            if self.grid[r][c] == 0:
                self.grid[r][c] = 2  # dynamic wall
                return (r, c)
        return None
