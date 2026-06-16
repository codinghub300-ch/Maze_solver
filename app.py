import streamlit as st
import heapq

# ==========================
# Maze Solver
# ==========================

class MazeSolver:

    def __init__(self, maze):
        self.maze = maze
        self.rows = len(maze)
        self.cols = len(maze[0])
        self.start = None
        self.end = None

        self.find_start_end()

    def find_start_end(self):
        for r in range(self.rows):
            for c in range(self.cols):

                if self.maze[r][c] == "A":
                    self.start = (r, c)

                elif self.maze[r][c] == "B":
                    self.end = (r, c)

    def get_neighbors(self, pos):

        row, col = pos

        directions = [
            (0, 1),
            (1, 0),
            (0, -1),
            (-1, 0)
        ]

        neighbors = []

        for dr, dc in directions:

            nr = row + dr
            nc = col + dc

            if (
                0 <= nr < self.rows
                and
                0 <= nc < self.cols
                and self.maze[nr][nc] != "#"
            ):
                neighbors.append((nr, nc))

        return neighbors

    def bfs(self):

        queue = [(self.start, [self.start])]
        visited = {self.start}

        while queue:

            current, path = queue.pop(0)

            if current == self.end:
                return path

            for neighbor in self.get_neighbors(current):

                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(
                        (neighbor, path + [neighbor])
                    )

        return None

    def dfs(self):

        stack = [(self.start, [self.start])]
        visited = {self.start}

        while stack:

            current, path = stack.pop()

            if current == self.end:
                return path

            for neighbor in self.get_neighbors(current):

                if neighbor not in visited:
                    visited.add(neighbor)
                    stack.append(
                        (neighbor, path + [neighbor])
                    )

        return None

    def a_star(self):

        def heuristic(a, b):
            return (
                abs(a[0] - b[0])
                +
                abs(a[1] - b[1])
            )

        open_set = []

        heapq.heappush(
            open_set,
            (0, self.start, [self.start])
        )

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

                tentative = g_cost[current] + 1

                if (
                    neighbor not in g_cost
                    or tentative < g_cost[neighbor]
                ):

                    g_cost[neighbor] = tentative

                    f_cost = tentative + heuristic(
                        neighbor,
                        self.end
                    )

                    heapq.heappush(
                        open_set,
                        (
                            f_cost,
                            neighbor,
                            path + [neighbor]
                        )
                    )

        return None


# ==========================
# Preset Mazes
# ==========================

mazes = {

    "Simple Maze":
"""#######
#A...B#
#.#.#.#
#.....#
#######""",

    "Medium Maze":
"""##########
#A......B#
#.#######.
#.#......#
#.#.######
#.#......#
##########""",

    "Complex Maze":
"""################
#A.......#....B#
#.####.#.#.###.#
#.#....#.#.....#
#.#.######.#####
#.#.............#
#.#.###########.#
#...............#
################"""
}

# ==========================
# Streamlit UI
# ==========================

st.set_page_config(
    page_title="Maze Solver",
    page_icon="🧩"
)

st.title("🧩 Maze Solver")

st.write(
    "Solve mazes using BFS, DFS, or A* Search."
)

maze_choice = st.selectbox(
    "Choose Maze",
    list(mazes.keys()) + ["Custom Maze"]
)

if maze_choice == "Custom Maze":

    maze_text = st.text_area(
        "Enter Your Maze",
        height=250
    )

else:

    maze_text = st.text_area(
        "Maze Layout",
        value=mazes[maze_choice],
        height=250
    )

algorithm = st.selectbox(
    "Choose Algorithm",
    ["BFS", "DFS", "A*"]
)

if st.button("🔍 Solve Maze"):

    try:

        maze = [
            list(row)
            for row in maze_text.strip().splitlines()
        ]

        solver = MazeSolver(maze)

        if algorithm == "BFS":
            solution = solver.bfs()

        elif algorithm == "DFS":
            solution = solver.dfs()

        else:
            solution = solver.a_star()

        if solution:

            solved = [row[:] for row in maze]

            for r, c in solution:

                if solved[r][c] not in ("A", "B"):
                    solved[r][c] = "*"

            st.success("✅ Solution Found!")

            st.write(
                f"Algorithm Used: {algorithm}"
            )

            st.write(
                f"Path Length: {len(solution)}"
            )

            st.subheader("Solved Maze")

            st.code(
                "\n".join(
                    "".join(row)
                    for row in solved
                )
            )

        else:

            st.error(
                "❌ No solution found."
            )

    except Exception as e:

        st.error(
            f"Invalid Maze Format: {e}"
        )
      
