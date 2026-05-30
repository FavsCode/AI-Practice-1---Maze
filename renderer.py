import os
import copy
import time
from agent import Agent
import colorama

class Renderer:
    def __init__(self, Agent: Agent, maze):
        colorama.init()
        self.start_color = colorama.Fore.BLUE + colorama.Style.BRIGHT
        self.pos_color = colorama.Fore.GREEN + colorama.Style.BRIGHT
        self.goal_color = colorama.Fore.RED + colorama.Style.BRIGHT
        self.print_maze = copy.deepcopy(maze) # Create a copy of the maze to show the current position

        MAZE_DELAY = 0.3 # Set a delay time (in seconds) for visualizing the maze updates; adjust as needed

        # Apply colors to the maze
        for i in range(len(self.print_maze)):
            for j in range(len(self.print_maze[i])):
                if self.print_maze[i][j] == "S":
                    self.print_maze[i][j] = self.start_color + "S" + colorama.Style.RESET_ALL # Color the starting position
                if self.print_maze[i][j] == "G":
                    self.print_maze[i][j] = self.goal_color + "G" + colorama.Style.RESET_ALL # Color the goal position
                if self.print_maze[i][j] == "#":
                    self.print_maze[i][j] = colorama.Style.DIM + "#" + colorama.Style.RESET_ALL # Color the walls

    def render_maze_state(self, Agent, maze, MAZE_DELAY):
        print(f"Steps taken: {Agent.steps}") # Debugging: Show the number of steps

        for row in self.print_maze:
                print("".join(row)) # Print the initial maze state

        time.sleep(3) # Pause to allow the user to see the initial maze before the agent starts moving
        
        while True:
            print(f"Steps taken: {Agent.steps}") # Debugging: Show the number of steps
            position = Agent.position
            move = Agent.choose_move(maze)

            if move is None:
                print("No more moves available. Stuck!")
                break
            
            self.print_maze[position[0]][position[1]] = self.pos_color + "." + colorama.Style.RESET_ALL # Mark the current position in the maze copy with a dot to visualize the path taken

            for row in self.print_maze:
                print("".join(row)) # Print the updated maze state

            # MAZE DELAY HERE. Turn off if you need. Change the time delay to adjust the speed of the visualization
            time.sleep(MAZE_DELAY)

            if maze[position[0]][position[1]] == "G":
                print("Goal reached!")
                break
            if Agent.steps >= 1000: # Set a maximum number of steps to prevent infinite loops in case of issues
                print("Maximum steps reached. Stopping to prevent infinite loop.")
                break

            self.print_maze[position[0]][position[1]] = colorama.Style.DIM + "." + colorama.Style.RESET_ALL # Un-highlight the current position after moving, so the path is shown as dots
