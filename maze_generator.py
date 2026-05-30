"""Handles maze generation and representation."""
"""Maze requirements:
    1. The maze should be represented as a 2D grid as a list of lists.
    2. The maze should have a defined starting point (S) and a goal point (G).
    3. The maze should include walls (represented by "#") that the agent cannot pass through.
    4. The maze should include open paths (represented by " ") that the agent can navigate through to reach the goal.
    5. The maze should have at least one valid path from the starting point to the goal.
    6. The maze should be enclosed by walls to prevent the agent from moving outside the boundaries of the maze.
"""
import random

class Maze:
    def __init__(self, randomness: float = 0.3): # Default ratio of spaces to walls is 30% spaces and 70% walls
        """Initalize the maze"""
        self.MAZE_WIDTH = random.randint(10, 20) 
        self.MAZE_HEIGHT = random.randint(5, 15)
        self.START_POS = (1, 1)
        self.GOAL_POS = (random.randint(1, self.MAZE_HEIGHT - 2), self.MAZE_WIDTH - 2)

        self.randomness: float = randomness # Extra spaces %

    def init_maze(self) -> None:
        """Creates the actual maze."""
        self.maze = [["#" for i in range(self.MAZE_WIDTH)] for i in range(self.MAZE_HEIGHT)]

        # Add a goal and starting position
        self.maze[self.START_POS[0]][self.START_POS[1]] = "S" 
        self.maze[self.GOAL_POS[0]][self.GOAL_POS[1]] = "G"

    def create_winning_path(self) -> None:
        "Makes paths from the starting position to the goal."
        current_pos = self.START_POS

        while current_pos != self.GOAL_POS:
            x, y = current_pos
            if self.maze[x][y] != "S" and self.maze[x][y] != "G":
                self.maze[x][y] = " " # Mark the current position as a space

            # Determine the next step towards the goal
            if random.random() < 0.5:
                if x < self.GOAL_POS[0]:
                    x += 1
                elif x > self.GOAL_POS[0]:
                    x -= 1
            else:
                if y != self.GOAL_POS[1]:
                    y += 1
                elif y > self.GOAL_POS[1]:
                    y -= 1  
    
            current_pos = (x, y)
    
    def add_random_paths(self) -> None:
        """Adds random paths to the maze based on the SPACE_TO_WALL_RATIO."""
        for i in range(1, self.MAZE_HEIGHT - 1):
            for j in range(1, self.MAZE_WIDTH - 1):
                if self.maze[i][j] == "#": # Only consider walls for conversion to spaces
                    if random.random() < self.randomness:
                        self.maze[i][j] = " " # Convert wall to space based on the ratio of spaces to walls
    
    def construct_maze(self) -> list[list[str]]:
        """Constructs the maze by initializing it, creating a winning path, and adding random paths."""
        self.init_maze()
        self.create_winning_path()
        self.add_random_paths()
        return self.maze
