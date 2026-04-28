import random
import copy
import time
import os
import colorama

def clear():
    os.system("cls" if os.name == "nt" else "clear")

class Agent:
    available_moves = []

    def __init__(self):
        self.visited_count = dict() # Keep track of visited positions to avoid cycles; use a dictionary to count visits to each position

AI = Agent() # Create an instance of the Agent class to keep track of visited positions

maze = [
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"],
    ["#", "S", " ", " ", "#", " ", " ", " ", "G", "#"],
    ["#", " ", "#", " ", "#", " ", "#", " ", "#", "#"],
    ["#", " ", "#", " ", " ", " ", "#", " ", " ", "#"],
    ["#", " ", "#", "#", "#", " ", "#", "#", " ", "#"],
    ["#", " ", " ", " ", " ", " ", " ", " ", " ", "#"],
    ["#", "#", "#", "#", "#", "#", "#", "#", "#", "#"]
]

def find_start(maze):
    for i in range(len(maze)):
        for j in range(len(maze[i])):
            if maze[i][j] == "S":
                return (i, j)
    return None

def find_available_spaces(maze, position):
    x, y = position
    spaces = []

    if maze[x-1][y] == "G":
        return [(x-1, y)] # If the goal is directly left, return it immediately as the only available move
    elif maze[x-1][y] != "#":
        spaces.append((x-1, y))
    
    if maze[x+1][y] == "G":
        return [(x+1, y)] # If the goal is directly right, return it immediately as the only available move
    elif maze[x+1][y] != "#":
        spaces.append((x+1, y))
    
    if maze[x][y-1] == "G":
        return [(x, y-1)] # If the goal is directly below, return it immediately as the only available move
    elif maze[x][y-1] != "#":
        spaces.append((x, y-1))
    
    if maze[x][y+1] == "G":
        return [(x, y+1)] # If the goal is directly above, return it immediately as the only available move
    elif maze[x][y+1] != "#":
        spaces.append((x, y+1))
    
    return spaces

def choose_move(maze, position, steps):

    available_spaces = find_available_spaces(maze, position)
    for pos in available_spaces:
        if pos not in AI.visited_count:
            AI.visited_count[pos] = 0 # Initialize visit count for new positions that become available

    if not available_spaces:
        return None
    if maze[position[0]][position[1]] == "G":
        return position  # Goal reached
    
    current_pos = (position[0], position[1])

    if current_pos not in AI.visited_count:
        AI.visited_count[current_pos] = 0 

    AI.visited_count[current_pos] += 1 # Mark the current position as visited and add the penalty for visiting it again
    
    # print("Visited count:", AI.visited_count) # Debugging: Show the visited count for each position
    
    values = {}

    for pos in available_spaces:
        if pos not in values:
            values[pos] = 0 # In the beginning, all moves are the optimal move
    
    for pos in values: # Create the list of optimal moves based on the values calculated
        visit_score = AI.visited_count[pos] # Calculate a score based on how many times the move has been visited
        values[pos] -= visit_score # Subtract the visit score from the move's value to penalize moves that have been visited more often
    
    print(f"Move values: {values}") # Debugging: Show the values of available moves

    exploration_rate = max(0.05, 0.25 - steps * 0.002) # Decrease exploration rate over time, but never go below 5%
    if len(values) <= 2:
        exploration_rate = 0.1 # Lower exploration rate when there are fewer moves available to encourage more exploitation of the best moves

    if random.random() < exploration_rate: # decreasing exploration rate over time, but never below 5%
        return random.choice(available_spaces)
    else:
        move = max(values, key=lambda pos:values[pos]) # Choose the move with the highest value (smallest penalty)
        print(f"Chosen move: {move} with value: {values[move]}") # Debugging: Show the chosen move and its value
        moves = [pos for pos in values if values[pos] == values[move]] # Get all moves that have the same lowest value
        print(f"Best moves: {moves}") # Debugging: Show all the best moves with the same value
        best_move = random.choice(moves) # Randomly choose among the best moves if there are multiple with the same value
        return best_move
        

def main():
    clear() # Clear the console at the start of the program
    colorama.init()
    start_color = colorama.Fore.BLUE + colorama.Style.BRIGHT
    pos_color = colorama.Fore.GREEN + colorama.Style.BRIGHT
    goal_color = colorama.Fore.RED + colorama.Style.BRIGHT
    position = find_start(maze)
    print_maze = copy.deepcopy(maze) # Create a copy of the maze to show the current position
    steps = 0
    max_steps = 100 # Set a maximum number of steps to prevent infinite loops in case of issues
    MAZE_DELAY = 0.3 # Set a delay time (in seconds) for visualizing the maze updates; adjust as needed

    for i in range(len(print_maze)):
        for j in range(len(print_maze[i])):
            if print_maze[i][j] == "S":
                print_maze[i][j] = start_color + "S" + colorama.Style.RESET_ALL # Color the starting position
            if print_maze[i][j] == "G":
                print_maze[i][j] = goal_color + "G" + colorama.Style.RESET_ALL # Color the goal position
            if print_maze[i][j] == "#":
                print_maze[i][j] = colorama.Style.DIM + "#" + colorama.Style.RESET_ALL # Color the walls

    for row in print_maze:
            print("".join(row)) # Print the initial maze state

    time.sleep(3) # Pause to allow the user to see the initial maze before the agent starts moving
    clear() # Clear the console to show the updated maze state
    while True:
        move = choose_move(maze, position, steps)

        if move is None:
            print("No more moves available. Stuck!")
            break
        
        position = move
        steps += 1
        print(f"Steps taken: {steps}") # Debugging: Show the number of steps taken so far

        print ("Moving to:", position)
        print(move) # Debugging: Show the move chosen
        print_maze[move[0]][move[1]] = pos_color + "." + colorama.Style.RESET_ALL # Mark the current position in the maze copy with a dot to visualize the path taken

        for row in print_maze:
            print("".join(row))

        # MAZE DELAY HERE. Turn off if you need. Change the 
        time.sleep(MAZE_DELAY)

        if maze[move[0]][move[1]] == "G":
            print("Goal reached!")
            break
        if steps >= max_steps:
            print("Maximum steps reached. Stopping to prevent infinite loop.")
            break
        print_maze[move[0]][move[1]] = colorama.Style.DIM + "." + colorama.Style.RESET_ALL # Un-highlight the current position after moving, so the path is shown as dots
        clear() # Clear the console to show the updated maze state


if __name__ == "__main__":    
    main()