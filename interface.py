import tkinter as tk
from tkinter import simpledialog, messagebox
import heapq

# Maze Solver Class (Same as your original code)
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


# GUI Functions
class MazeGUI(tk.Tk):
    def __init__(self, maze):
        super().__init__()
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.solver = MazeSolver(maze)

        self.title("Maze Solver")
        self.geometry("500x500")

        self.canvas = tk.Canvas(self, width=400, height=400)
        self.canvas.pack(pady=20)

        self.draw_maze()

        # Algorithm selection buttons
        self.bfs_button = tk.Button(self, text="Solve with BFS", command=self.solve_bfs)
        self.bfs_button.pack(side=tk.LEFT, padx=10)

        self.dfs_button = tk.Button(self, text="Solve with DFS", command=self.solve_dfs)
        self.dfs_button.pack(side=tk.LEFT, padx=10)

        self.a_star_button = tk.Button(self, text="Solve with A*", command=self.solve_a_star)
        self.a_star_button.pack(side=tk.LEFT, padx=10)

    def draw_maze(self):
        self.canvas.delete("all")
        cell_size = 20
        for r in range(self.rows):
            for c in range(self.cols):
                color = 'white'
                if self.maze[r][c] == '#':
                    color = 'black'
                elif self.maze[r][c] == 'A':
                    color = 'green'
                elif self.maze[r][c] == 'B':
                    color = 'red'

                self.canvas.create_rectangle(c*cell_size, r*cell_size, (c+1)*cell_size, (r+1)*cell_size, fill=color)
                self.canvas.create_text(c*cell_size + 10, r*cell_size + 10, text=self.maze[r][c], font=('Arial', 10))

    def highlight_solution(self, solution):
        cell_size = 20
        for r, c in solution:
            self.canvas.create_rectangle(c*cell_size, r*cell_size, (c+1)*cell_size, (r+1)*cell_size, fill='blue')

    def solve_bfs(self):
        solution = self.solver.bfs()
        if solution:
            self.highlight_solution(solution)
        else:
            messagebox.showinfo("Result", "No solution found!")

    def solve_dfs(self):
        solution = self.solver.dfs()
        if solution:
            self.highlight_solution(solution)
        else:
            messagebox.showinfo("Result", "No solution found!")

    def solve_a_star(self):
        solution = self.solver.a_star()
        if solution:
            self.highlight_solution(solution)
        else:
            messagebox.showinfo("Result", "No solution found!")


# Function to take user input for the maze
def get_user_input():
    # Ask for the number of rows and columns
    rows = simpledialog.askinteger("Input", "Enter the number of rows in the maze:")
    if rows is None:
        return None  # User canceled the input
    cols = simpledialog.askinteger("Input", "Enter the number of columns in the maze:")
    if cols is None:
        return None  # User canceled the input

    maze = []
    for r in range(rows):
        row = simpledialog.askstring("Input", f"Enter row {r+1} (use '#' for walls, 'A' for start, 'B' for end):")
        if row is None:
            return None  # User canceled the input
        if len(row) != cols:
            messagebox.showerror("Error", f"Row {r+1} must have exactly {cols} characters.")
            return None
        maze.append(list(row))

    # Validate that there is exactly one start ('A') and one end ('B')
    start_count = sum(row.count('A') for row in maze)
    end_count = sum(row.count('B') for row in maze)
    if start_count != 1 or end_count != 1:
        messagebox.showerror("Error", "The maze must contain exactly one start ('A') and one end ('B').")
        return None

    return maze


if __name__ == "__main__":
    # Get maze input from the user
    maze_input = get_user_input()
    if maze_input:
        app = MazeGUI(maze_input)
        app.mainloop()
    else:
        print("No valid maze input. Exiting.")
