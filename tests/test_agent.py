"""Tests for the Agent."""
from agent import Agent
from tests.mazes import maze_1 as maze # All three test mazes should be cycled through, and all should pass the tests.
import copy

def test_agent_initialization() -> None:
    agent = Agent(maze)
    assert agent.position == (1, 1) # The starting position "S" is at (1, 1)
    assert agent.visited_count == {} # The visited count should be initialized as an empty dictionary
    assert agent.steps == 0 # The steps should be initialized to 0

def test_find_available_spaces() -> None:
    agent = Agent(maze)
    available_spaces = agent.find_available_spaces(maze)
    expected_spaces = [(1, 2), (2, 1)] # From the starting position (1, 1), the available spaces are to the right and down
    assert set(available_spaces) == set(expected_spaces)

def test_choose_move() -> None:
    agent = Agent(maze)
    move = agent.choose_move(maze)
    
    assert move in [(1, 2), (2, 1)] # The chosen move should be one of the available spaces from the starting position
    assert agent.visited_count[(1, 1)] == 1 # The starting position should now be marked as visited
    assert agent.steps == 1 # The Agent just took a step

def test_agent_reaching_goal() -> None:
    agent = Agent(maze)
    # Manually set the agent's position to be next to the goal for testing
    agent.position = (1, 8) # Position next to the goal "G"
    move = agent.choose_move(maze)
    assert move == (1, 8) # The chosen move should be the goal position itself

def test_agent_stuck() -> None:
    agent = Agent(maze)
    # Manually set the agent's position to be surrounded by walls for testing
    agent.position = (0, 0) # Position in the top-left corner, surrounded by walls
    move = agent.choose_move(maze)
    assert move is None # The agent should return None when there are no available moves   

def test_no_start_position() -> None:
    # Test that the Agent raises an error if there is no starting position "S" in the maze
    invalid_maze = [
        ["#", "#", "#"],
        ["#", " ", "#"],
        ["#", "#", "#"]
    ]
    try:
        agent = Agent(invalid_maze) # Agent not accessed because the init should fail
        assert False, "Expected ValueError for missing start position 'S'"
    except ValueError as e:
        assert str(e) == "Start position 'S' not found in the maze." 

def test_agent_memory() -> None:
    agent = Agent(maze)
    # Simulate the agent visiting a position multiple times
    agent.position = (1, 2) # Move to an available space
    agent.choose_move(maze) # First visit to (1, 2)
    print(agent.visited_count) # Debugging: Show the visited count after the first visit
    agent.position = (1, 2) # Move back to the same position
    agent.choose_move(maze) # Second visit to (1, 2)
    print(agent.visited_count) # Debugging: Show the visited count after the second visit
    
    assert agent.visited_count[(1, 2)] == 2 # The visited count for (1, 2) should be 2 after visiting it twice

def test_agent_move_values() -> None:
    agent = Agent(maze)
    # Simulate the agent calculating move values for available spaces
    agent.position = (1, 2) # Move to an available space
    available_spaces = agent.find_available_spaces(maze)
    move = agent.choose_move(maze) 
    
    assert move in available_spaces # The calculated move should be one of the available spaces

def test_agent_solve_maze() -> None:
    # This test uses visuals to show the agent solving the maze and to clearly expose errors such as a move into a wall.
    agent = Agent(maze)

    print_maze = copy.deepcopy(maze)
    for row in print_maze:
        print("".join(row)) # Print the initial maze state for debugging purposes

    # Simulate the agent trying to solve the maze by repeatedly choosing moves until it reaches the goal
    while True:
        agent.find_available_spaces(maze)
        
        move = agent.choose_move(maze)
        if move is None:
            break # The agent is stuck, exit the loop
        else:
            print(f"Agent moved to: {(move[0], move[1])}, Steps taken: {agent.steps}") # Debugging: Show the agent's position and steps after each move
            pass # The agent has made a move, continue to the next iteration to choose the next move
        
        print_maze[move[0]][move[1]] = "."
        for row in print_maze:
            print("".join(row)) # Print the initial maze state

        if maze[agent.position[0]][agent.position[1]] == "G":
            break # The agent has reached the goal, exit the loop
    
    assert maze[agent.position[0]][agent.position[1]] == "G" # The agent should have reached the goal at the end of this process

def test_agent_step_counter() -> None:
    agent = Agent(maze)
    initial_steps = agent.steps
    agent.choose_move(maze) # Make a move
    assert agent.steps == initial_steps + 1 # The steps counter should increment by 1 after a move