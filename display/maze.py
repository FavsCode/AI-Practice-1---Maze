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
    def __init__(self, SPACE_TO_WALL_RATIO):
        """Initalize the maze"""
        self.MAZE_WIDTH = random.randint(10, 20) 
        self.MAZE_HEIGHT = random.randint(5, 15)
        self.START_POS = (1, 1)
        self.GOAL_POS = (random.randint(1, self.MAZE_HEIGHT - 2), self.MAZE_WIDTH - 2)

        self.SPACE_TO_WALL_RATIO: float = SPACE_TO_WALL_RATIO

    def init_maze(self) -> None:
        """Creates the actual maze."""
        self.maze = [["#" for i in range(self.MAZE_WIDTH)] for i in range(self.MAZE_HEIGHT)]

        # Add a goal and starting position
        self.maze[self.START_POS[0]][self.START_POS[1]] = "S" 
        self.maze[self.GOAL_POS[0]][self.GOAL_POS[1]] = "G"

    def create_maze_paths(self) -> list[list[str]]:
        "Makes paths from the starting position to the goal."
        reccomended_space_amount = self.MAZE_WIDTH * self.MAZE_HEIGHT * self.SPACE_TO_WALL_RATIO # As in the percentage of the total maze that are spaces

        while range(int(reccomended_space_amount)):
            i = random.randint(1, self.MAZE_HEIGHT - 2)
            j = random.randint(1, self.MAZE_WIDTH - 2)

            if self.maze[i][j] == "S" or self.maze[i][j] == "G":
                continue # As to not erase the starting or goal position
            else:
                self.maze[i][j] = " "

        # Ensure goal and starting position have at least one exit
        self.maze[self.START_POS[0]][self.START_POS[1] + 1] = " " # Guarenteed next to the start position
        self.maze[self.GOAL_POS[0]][self.GOAL_POS[1] - 1] = " "

        return self.maze


