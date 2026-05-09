"""Handles the Agent class, including its memory and decision-making process for navigating the maze."""
from display.mazes import maze_1 as maze # Temporary import for testing purposes
import random

class Agent:
    def __init__(self, maze):
        """ Initialize the Agent with the maze and set up its memory and current state. """
        # Memory
        self.visited_count: dict[tuple, int] = {}
        self.move_values = {}

        # Current state
        self.maze: list[list] = maze
        self.init_start_pos(maze) 
        self.steps = 0 # Keep track of the number of steps taken to adjust exploration rate over time

    def init_start_pos(self, maze) -> None:
        """ Initialize the agent's starting position based on the location of "S" in the maze. """
        for i in range(len(maze)):
            for j in range(len(maze[i])):
                if maze[i][j] == "S":
                    self.position = (i, j)
        try: 
            self.position
        except AttributeError: # If the position attribute was not set, it means the start position "S" was not found in the maze
            raise ValueError("Start position 'S' not found in the maze.")
    
    def find_available_spaces(self, maze) -> list[tuple]:
        """ Find available spaces around the current position that are not walls. If the goal is found, return it immediately as the only available move."""
        x, y = self.position # type: ignore 
        spaces = []
        spaces_to_check = [(x-1, y), (x+1, y), (x, y-1), (x, y+1)]
        for space in spaces_to_check:
            if maze[space[0]][space[1]] == "G":
                return [(space[0], space[1])] # If the goal is found, set the position to the goal and return immediately
            elif maze[space[0]][space[1]] != "#":
                spaces.append((space[0], space[1]))
        
        return spaces

    def choose_move(self) -> tuple | None:
        """ Choose the next move based on the available spaces and the visited count to encourage exploration and exploitation. """
        available_spaces = self.find_available_spaces(maze)
        
        for pos in available_spaces:
            if pos not in self.visited_count:
                self.visited_count[pos] = 0 # Initialize visit count for new positions that become available
        if not available_spaces:
            return None # No available moves, return None to indicate that the agent is stuck
        
        current_pos = (self.position[0], self.position[1])
        if current_pos not in self.visited_count:
            self.visited_count[current_pos] = 0 # Initialize visit count for the current position if it hasn't been visited before
            
        if maze[self.position[0]][self.position[1]] == "G":
            return self.position  # Goal reached, return the current position as the move to make
        
        move = self.calculate_move_values(available_spaces)
    
        self.steps += 1
        self.visited_count[current_pos] += 1 # Mark the current position as visited and add the penalty for visiting it again
        
    def calculate_move_values(self, available_spaces) -> tuple:
        """ Calculate values for each available move based on the visited count and other factors to encourage exploration and exploitation. """
        # Function depends on the visited_count dictionary, which is updated in the choose_move method, so it should be called using the choose_move method.
        values = {}

        for pos in available_spaces:
            if pos not in values:
                values[pos] = 0 # In the beginning, all moves are the optimal move
        
        for pos in values: # Create the list of optimal moves based on the values calculated
            visit_score = self.visited_count[pos] 
            values[pos] -= visit_score

        exploration_rate = max(0.05, 0.25 - self.steps * 0.002) # Decrease exploration rate over time, but never go below 5%
        if len(values) <= 2:
            exploration_rate = 0.1 # Lower exploration rate when there are fewer moves available to encourage more exploitation of the best moves

        if random.random() < exploration_rate: # Explore
            return random.choice(available_spaces)
        else: # Exploit
            move = max(values, key=lambda pos:values[pos]) # Choose the move with the highest value (smallest penalty)
            moves: list[tuple] = [pos for pos in values if values[pos] == values[move]] # Get all moves that have the same lowest value
            best_move = random.choice(moves)
            return best_move
        