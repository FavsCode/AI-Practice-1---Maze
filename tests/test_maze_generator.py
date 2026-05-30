"""Test for the maze generator."""
from maze_generator import Maze
from agent import Agent

def test_maze_init() -> None:
    maze_generator = Maze(randomness=0.3)
    maze_generator.construct_maze()
    
    # Check that the maze has the correct dimensions
    assert len(maze_generator.maze) == maze_generator.MAZE_HEIGHT
    assert all(len(row) == maze_generator.MAZE_WIDTH for row in maze_generator.maze)
    
    # Check that the starting position and goal position are correctly set
    assert maze_generator.maze[maze_generator.START_POS[0]][maze_generator.START_POS[1]] == "S"
    assert maze_generator.maze[maze_generator.GOAL_POS[0]][maze_generator.GOAL_POS[1]] == "G"

def test_maze_paths() -> None:
    maze_generator = Maze(randomness=0.3)
    maze = maze_generator.construct_maze()
    
    # Check that the maze still has the correct dimensions after creating paths
    assert len(maze) == maze_generator.MAZE_HEIGHT
    assert all(len(row) == maze_generator.MAZE_WIDTH for row in maze)
    
    # Check that the starting position and goal position are still correctly set
    assert maze[maze_generator.START_POS[0]][maze_generator.START_POS[1]] == "S"
    assert maze[maze_generator.GOAL_POS[0]][maze_generator.GOAL_POS[1]] == "G"
    
    # Check that there are spaces in the maze (not all walls)
    space_count = sum(row.count(" ") for row in maze)
    assert space_count > 0, "There should be at least one space in the maze."

def test_maze_beatable() -> None:
    maze_generator = Maze(randomness=0.3)
    maze = maze_generator.construct_maze()

    # CODE PASTED FROM test_agent.py's test_agent_solve_maze() function to check if the maze is beatable
    agent = Agent(maze)

    # Simulate the agent trying to solve the maze by repeatedly choosing moves until it reaches the goal
    while agent.steps < 1000: # Limit the number of steps to prevent infinite loops in case the maze is unsolvable
        agent.find_available_spaces(maze)
        
        move = agent.choose_move(maze)
        if move is None:
            break # The agent is stuck, exit the loop
        else:
            pass # The agent has made a move, continue to the next iteration to choose the next move

        if maze[agent.position[0]][agent.position[1]] == "G":
            break # The agent has reached the goal, exit the loop
    
    assert maze[agent.position[0]][agent.position[1]] == "G" # The agent should have reached the goal at the end of this process
    
    
    