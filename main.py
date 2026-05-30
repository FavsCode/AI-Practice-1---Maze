from agent import Agent
from renderer import Renderer
from maze_generator import Maze

def main():
    MAZE_DELAY = 0.5  # Set a delay time (in seconds) for visualizing the maze updates; adjust as needed
    MAZE_RANDOMNESS = 0.3  # Set the randomness ratio for the maze (e.g., 0.3 for 30% random spaces and 70% walls)

    # Create a maze with a specified randomness ratio (e.g., 0.3 for 30% random spaces and 70% walls)
    maze_generator = Maze(MAZE_RANDOMNESS)
    maze = maze_generator.construct_maze()

    # Initialize the agent with the generated maze
    agent = Agent(maze)

    # Initialize the renderer with the agent and the maze
    renderer = Renderer(agent, maze)

    # Render the maze state and visualize the agent's movement
    renderer.render_maze_state(agent, maze, MAZE_DELAY)  # Adjust MAZE_DELAY as needed

if __name__ == "__main__":
    main()