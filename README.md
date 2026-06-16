# Maze Solver 

Live Demo:
https://advanture-qlw3izvbae2sulncwq32rq.streamlit.app/

A Python-based Maze Solver application that finds and visualizes the path between a start point and an end point using different search algorithms.

---

##  Features

- Solve mazes using:
  - Breadth-First Search (BFS)
  - Depth-First Search (DFS)
  - A* Search Algorithm
- Interactive GUI using Tkinter
- Console-based version for algorithm testing
- User-defined maze input
- Visual representation of the solution path
- Supports walls, paths, start, and destination points

---

##  Technologies Used

- Python
- Tkinter
- Heap Queue (heapq)
- Data Structures & Algorithms

---

## Maze Symbols
| Symbol | Meaning           |
| ------ | ----------------- |
| A      | Start Point       |
| B      | Destination Point |
| #      | Wall/Obstacle     |
| *      | Solution Path     |

## Algorithms Used
1. Breadth-First Search (BFS)
Explores nodes level by level.
Guarantees the shortest path in unweighted mazes.

2. Depth-First Search (DFS)
Explores as deep as possible before backtracking.
Faster in some cases but may not find the shortest path.

3. A* Search Algorithm
Uses heuristics to find the most optimal path efficiently.
Combines path cost and estimated distance to destination.

##  How to Run

### Run GUI Version

```bash
python interface.py
