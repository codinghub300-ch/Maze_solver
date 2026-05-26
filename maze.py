import queue
import heapq

# Maze Solver Class
class MazeSolver:
    def __init__(self, maze):
        self.maze = maze
        self.start = None
        self.end = None
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.find_start_end()

    def find_start_end(self):
        for r in range(self.rows):
            for c in range(self.cols):
                if self.maze[r][c] == 'A':
                    self.start = (r, c)
                elif self.maze[r][c] == 'B':
                    self.end = (r, c)

    def get_neighbors(self, position):
        row, col = position
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
        neighbors = []
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.rows and 0 <= nc < self.cols and self.maze[nr][nc] != '#':
                neighbors.append((nr, nc))
        return neighbors

    def bfs(self):
        queue = [(self.start, [self.start])]
        visited = set()
        visited.add(self.start)

        while queue:
            current, path = queue.pop(0)
            if current == self.end:
                return path

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, path + [neighbor]))

        return None

    def dfs(self):
        stack = [(self.start, [self.start])]
        visited = set()
        visited.add(self.start)

        while stack:
            current, path = stack.pop()
            if current == self.end:
                return path

            for neighbor in self.get_neighbors(current):
                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append((neighbor, path + [neighbor]))

        return None

    def a_star(self):
        def heuristic(pos1, pos2):
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

        open_set = []
        heapq.heappush(open_set, (0, self.start, [self.start]))
        g_cost = {self.start: 0}
        visited = set()

        while open_set:
            _, current, path = heapq.heappop(open_set)
            if current in visited:
                continue

            if current == self.end:
                return path

            visited.add(current)

            for neighbor in self.get_neighbors(current):
                tentative_g_cost = g_cost[current] + 1
                if neighbor not in g_cost or tentative_g_cost < g_cost[neighbor]:
                    g_cost[neighbor] = tentative_g_cost
                    f_cost = tentative_g_cost + heuristic(neighbor, self.end)
                    heapq.heappush(open_set, (f_cost, neighbor, path + [neighbor]))

        return None

def open_maze_input():
    print("Enter the maze directly (end with an empty line):")
    maze = []
    while True:
        try:
            line = input()
            if line.strip() == "":
                break
            maze.append(list(line.strip()))
        except EOFError:
            break
    if not maze:
        print("No maze provided. Exiting.")
        return None
    return maze

def draw_solution(maze, solution):
    for r, row in enumerate(maze):
        for c, cell in enumerate(row):
            if (r, c) in solution and cell not in ('A', 'B'):
                maze[r][c] = '*'
    return maze

def display_maze(maze):
    for row in maze:
        print("".join(row))

if __name__ == "__main__":
    maze = open_maze_input()
    if maze:
        solver = MazeSolver(maze)
        print("Choose an algorithm: 1) BFS  2) DFS  3) A*")
        choice = input("Enter your choice: ")

        if choice == '1':
            solution = solver.bfs()
        elif choice == '2':
            solution = solver.dfs()
        elif choice == '3':
            solution = solver.a_star()
        else:
            print("Invalid choice!")
            exit()

        if solution:
            print("Solution found:", solution)
            maze = draw_solution(maze, solution)
            display_maze(maze)
        else:
            print("No solution found.")
