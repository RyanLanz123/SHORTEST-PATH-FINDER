import curses
from curses import wrapper
import queue
import time

# Define the maze layout using a 2D list
maze = [
    ["#", "O", "#", "#", "#", "#", "#", "#", "#"],  # 'O' is the starting point
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],  # ' ' represents open paths
    ["#", " ", "#", "#", " ", "#", "#", " ", "#"],  # '#' represents walls
    ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
    ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "X", "#"]   # 'X' is the ending point
]

# Function to print the maze on the screen
def print_maze(maze, stdscr, path=[]):
    """
    Display the maze on the screen with the current path highlighted.
    
    Args:
    - maze: The 2D list representing the maze layout.
    - stdscr: The curses screen object for displaying content.
    - path: A list of (row, col) tuples representing the current path.
    """
    BLUE = curses.color_pair(1)  # Define the color for walls and paths
    RED = curses.color_pair(2)   # Define the color for the solution path

    for i, row in enumerate(maze):  # Iterate through each row of the maze
        for j, value in enumerate(row):  # Iterate through each cell in the row
            if (i, j) in path:  # Highlight cells in the solution path
                stdscr.addstr(i, j*2, "X", RED)
            else:  # Display walls and open paths normally
                stdscr.addstr(i, j*2, value, BLUE)

# Function to find the starting position of the maze
def find_start(maze, start):
    """
    Locate the starting position ('O') in the maze.
    
    Args:
    - maze: The 2D list representing the maze layout.
    - start: The character representing the start position ('O').
    
    Returns:
    - A tuple (row, col) of the start position or None if not found.
    """
    for i, row in enumerate(maze):  # Iterate through each row
        for j, value in enumerate(row):  # Iterate through each cell
            if value == start:  # Return the position if it matches the start
                return i, j
    
    return None  # Return None if the start position is not found

# Main function to find the path from start to end
def find_path(maze, stdscr):
    """
    Use breadth-first search to find the shortest path from start ('O') to end ('X').
    
    Args:
    - maze: The 2D list representing the maze layout.
    - stdscr: The curses screen object for displaying progress.
    
    Returns:
    - A list of (row, col) tuples representing the path from start to end.
    """
    start = "O"  # Character representing the start
    end = "X"    # Character representing the end
    start_pos = find_start(maze, start)  # Find the starting position

    # Use a queue for breadth-first search
    q = queue.Queue()
    q.put((start_pos, [start_pos]))  # Add the starting position and path to the queue

    visited = set()  # Keep track of visited positions

    while not q.empty():
        current_pos, path = q.get()  # Get the current position and path
        row, col = current_pos

        # Display the current maze state with the path highlighted
        stdscr.clear()
        print_maze(maze, stdscr, path)
        time.sleep(0.2)  # Add a delay for visualization
        stdscr.refresh()

        if maze[row][col] == end:  # Check if the end is reached
            return path  # Return the path if the goal is found
        
        # Find and process neighbors
        neighbors = find_neighbors(maze, row, col)
        for neighbor in neighbors:
            if neighbor in visited:  # Skip already visited neighbors
                continue

            r, c = neighbor
            if maze[r][c] == "#":  # Skip walls
                continue

            new_path = path + [neighbor]  # Extend the path
            q.put((neighbor, new_path))  # Add the neighbor and path to the queue
            visited.add(neighbor)  # Mark the neighbor as visited

# Helper function to find neighboring cells
def find_neighbors(maze, row, col):
    """
    Get the neighboring cells for the given position.
    
    Args:
    - maze: The 2D list representing the maze layout.
    - row: The current row index.
    - col: The current column index.
    
    Returns:
    - A list of (row, col) tuples representing valid neighbors.
    """
    neighbors = []

    # Check each direction: UP, DOWN, LEFT, RIGHT
    if row > 0:  # UP
        neighbors.append((row - 1, col))
    if row + 1 < len(maze):  # DOWN
        neighbors.append((row + 1, col))
    if col > 0:  # LEFT
        neighbors.append((row, col - 1))
    if col + 1 < len(maze[0]):  # RIGHT
        neighbors.append((row, col + 1))

    return neighbors

# Main function for curses setup and running the pathfinding algorithm
def main(stdscr):
    """
    Initialize curses colors and run the pathfinding algorithm.
    
    Args:
    - stdscr: The curses screen object.
    """
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)  # Color pair for walls
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)   # Color pair for solution path

    find_path(maze, stdscr)  # Run the pathfinding algorithm
    stdscr.getch()  # Wait for user input before exiting

# Ensure the wrapper is called at the top level to initialize curses
wrapper(main)
