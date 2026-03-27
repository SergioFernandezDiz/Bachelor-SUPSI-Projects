# Project Structure

This document describes the modular package structure of the Frankie Robot Simulation project.

## Directory Structure

```
git_actual/
├── README.md                 # Main project documentation
├── requirements.txt         # Python dependencies
├── launcher.py              # GUI launcher for simulations
├── STRUCTURE.md             # This file
│
├── core/                     # Core utilities package
│   ├── __init__.py          # Exports: Vector3, a_star_search
│   ├── algebra.py           # Vector3 class and math utilities
│   └── astar.py             # A* path planning algorithm
│
├── frankie/                  # Frankie robot package
│   ├── __init__.py          # Exports: FrankieController, FrankieControllerParams, TaskState, FrankieAgent
│   ├── controller.py        # Main controller logic (state machine, IK, path planning)
│   └── agent.py             # FrankieAgent class for robot simulation
│
├── generators/               # Environment generators package
│   ├── __init__.py          # Exports: Obstacle, get_obstacles, obstacles_to_world_grid, get_maze
│   ├── obstacle_generator.py # Obstacle generation for obstacle avoidance simulation
│   └── maze_generator.py    # Maze generation for maze simulation
│
├── environments/             # Environment builders package
│   ├── __init__.py          # Exports: Wall3D, Env, build_maze_scene, etc.
│   └── maze.py              # Maze environment builder (walls, floors, scene construction)
│
├── plotting/                 # Plotting utilities package
│   ├── __init__.py          # Exports: plot_basic_metrics, plot_maze_metrics, plot_obstacles_2d
│   ├── basic.py             # Plotting for basic pick-and-place simulation
│   ├── maze.py              # Plotting for maze simulation
│   └── obstacle.py          # Obstacle visualization for obstacle avoidance simulation
│
└── scripts/                  # Simulation scripts (executable entry points)
    ├── __init__.py          # Empty (scripts not meant to be imported)
    ├── pick_and_place.py    # Basic pick-and-place simulation
    ├── obstacle_avoidance.py # Obstacle avoidance simulation
    └── maze.py              # Maze simulation with two robots
```

## Package Descriptions

### `core/`
Core utilities and algorithms used throughout the project:
- **`algebra.py`**: `Vector3` class and helper functions (`damped_pseudoinverse`, `wrap_angle`, etc.)
- **`astar.py`**: A* path planning algorithm for grid-based navigation

### `frankie/`
Robot-specific code:
- **`controller.py`**: `FrankieController` class implementing the state machine, inverse kinematics, resolved-rate control, and path planning integration
- **`agent.py`**: `FrankieAgent` class wrapping the robot model and Swift visualization

### `generators/`
Environment generation utilities:
- **`obstacle_generator.py`**: Generates random cylindrical obstacles for obstacle avoidance simulation
- **`maze_generator.py`**: Generates procedural mazes for maze simulation

### `environments/`
Environment builders for Swift 3D visualization:
- **`maze.py`**: Classes and functions for building maze environments (`Wall3D`, `Env`, `build_maze_scene`, etc.)

### `plotting/`
Visualization utilities:
- **`basic.py`**: Generates interactive HTML plots for basic pick-and-place simulation (supports obstacle visualization when obstacles are provided)
- **`maze.py`**: Generates interactive HTML plots for maze simulation
- **`obstacle.py`**: Obstacle visualization utilities (`plot_obstacles_2d`) for displaying obstacles and robot trajectory in obstacle avoidance simulations

### `scripts/`
Executable simulation scripts:
- **`pick_and_place.py`**: Basic pick-and-place task simulation
- **`obstacle_avoidance.py`**: Pick-and-place with obstacle avoidance using A* path planning
- **`maze.py`**: Two-robot maze navigation simulation


## Running Simulations

### Using the Launcher
```bash
python launcher.py
```

### Direct execution
```bash
# From project root
python scripts/pick_and_place.py
python scripts/obstacle_avoidance.py
python scripts/maze.py

