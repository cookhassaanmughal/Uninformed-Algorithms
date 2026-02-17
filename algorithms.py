from collections import deque
import heapq

# Clockwise including diagonals
MOVES = [
    (-1, 0),  # Up
    (0, 1),   # Right
    (1, 0),   # Down
    (1, 1),   # Bottom-Right
    (0, -1),  # Left
    (-1, -1), # Top-Left
    (-1, 1),  # Top-Right
    (1, -1)   # Bottom-Left
]

def reconstruct_path(parent, start, goal):
    path = []
    node = goal
    while node != start:
        path.append(node)
        node = parent[node]
    path.append(start)
    path.reverse()
    return path


# BFS
def bfs(grid):
    frontier = deque([grid.start])
    parent = {}
    visited = set([grid.start])

    while frontier:
        current = frontier.popleft()
        yield current, frontier, visited

        if current == grid.target:
            return reconstruct_path(parent, grid.start, grid.target)

        for move in MOVES:
            nr = current[0] + move[0]
            nc = current[1] + move[1]
            neighbor = (nr, nc)

            if grid.is_valid(neighbor) and neighbor not in visited:
                frontier.append(neighbor)
                visited.add(neighbor)
                parent[neighbor] = current

    return None


# DFS
def dfs(grid):
    frontier = [grid.start]
    parent = {}
    visited = set()

    while frontier:
        current = frontier.pop()
        yield current, frontier, visited

        if current == grid.target:
            return reconstruct_path(parent, grid.start, grid.target)

        if current not in visited:
            visited.add(current)
            for move in reversed(MOVES):
                neighbor = (current[0]+move[0], current[1]+move[1])
                if grid.is_valid(neighbor) and neighbor not in visited:
                    frontier.append(neighbor)
                    parent[neighbor] = current

    return None


# UCS
def ucs(grid):
    frontier = []
    heapq.heappush(frontier, (0, grid.start))
    parent = {}
    cost = {grid.start: 0}
    visited = set()

    while frontier:
        current_cost, current = heapq.heappop(frontier)
        yield current, [n[1] for n in frontier], visited

        if current == grid.target:
            return reconstruct_path(parent, grid.start, grid.target)

        if current not in visited:
            visited.add(current)
            for move in MOVES:
                neighbor = (current[0]+move[0], current[1]+move[1])
                if grid.is_valid(neighbor):
                    new_cost = current_cost + 1
                    if neighbor not in cost or new_cost < cost[neighbor]:
                        cost[neighbor] = new_cost
                        heapq.heappush(frontier, (new_cost, neighbor))
                        parent[neighbor] = current

    return None


# Depth Limited Search
def dls(grid, limit):
    def recursive(node, depth, parent, visited):
        yield node, [], visited
        if node == grid.target:
            return reconstruct_path(parent, grid.start, grid.target)
        if depth == limit:
            return None

        visited.add(node)

        for move in MOVES:
            neighbor = (node[0]+move[0], node[1]+move[1])
            if grid.is_valid(neighbor) and neighbor not in visited:
                parent[neighbor] = node
                result = yield from recursive(neighbor, depth+1, parent, visited)
                if result:
                    return result
        return None

    parent = {}
    visited = set()
    return (yield from recursive(grid.start, 0, parent, visited))


# IDDFS
def iddfs(grid):
    for depth in range(50):
        result = yield from dls(grid, depth)
        if result:
            return result
    return None


# Bidirectional BFS
def bidirectional(grid):
    start_front = {grid.start}
    goal_front = {grid.target}
    parent_start = {}
    parent_goal = {}
    visited_start = set([grid.start])
    visited_goal = set([grid.target])

    while start_front and goal_front:
        next_front = set()
        for node in start_front:
            yield node, start_front, visited_start
            for move in MOVES:
                neighbor = (node[0]+move[0], node[1]+move[1])
                if grid.is_valid(neighbor):
                    if neighbor in visited_goal:
                        parent_start[neighbor] = node
                        return reconstruct_path(parent_start, grid.start, neighbor)
                    if neighbor not in visited_start:
                        visited_start.add(neighbor)
                        parent_start[neighbor] = node
                        next_front.add(neighbor)
        start_front = next_front

    return None
