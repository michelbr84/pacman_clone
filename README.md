>>>>>>> branch-name
# pacman_clone
Clone do clássico jogo Pacman desenvolvido em Python com a biblioteca Pygame. Projeto modular e open source para aprendizado e contribuições.
=======
# Pacman Clone

This is a clone of the classic **Pacman** game, developed in Python using the **Pygame** library. The project is organized in a modular way by dividing the game logic into several scripts to simplify maintenance and future enhancements.

## Features

- **Pacman Movement:** Control the character using the arrow keys.
- **Simple Ghost AI:** Four ghosts move through the maze following predefined directional patterns.
- **Interactive Maze:** Includes walls, a gate, and pellets that can be collected.
- **Scoring System:** Your score increases as Pacman collects pellets.
- **Win/Lose Screens:** Display messages ("Congratulations, you won!" or "Game Over") that allow the player to restart or quit the game.

## Project Structure

```
Pacman-master/
│
├── main.py              # Main file that initializes and runs the game
└── scripts/
    ├── __init__.py      # Makes the scripts folder a Python package
    ├── config.py        # General settings and assets (colors, dimensions, fonts, etc.)
    ├── maze.py          # Maze creation (walls and gate)
    ├── block.py         # Definition of the blocks (pellets) forming the game grid
    ├── player.py        # Logic and behavior for Pacman
    ├── ghost.py         # Movement logic for ghosts (inherits from player.py)
    └── directions.py    # Direction lists used by the ghosts
```

## Requirements

- **Python 3.12+** (or another compatible version)
- **Pygame 2.6.1** (or a compatible version)

You can install Pygame using pip:

```bash
pip install pygame
```

## How to Run

1. Ensure that Python and Pygame are installed.
2. Navigate to the project's root directory (where `main.py` is located).
3. Run the game with:

   ```bash
   python main.py
   ```

## Game Controls

- **Left Arrow:** Move Pacman to the left.
- **Right Arrow:** Move Pacman to the right.
- **Up Arrow:** Move Pacman upward.
- **Down Arrow:** Move Pacman downward.
- **ENTER:** Restart the game after the win/lose screen.
- **ESCAPE:** Quit the game.

## Additional Information

- The game is divided into modules to facilitate future modifications and scalability.
- Make sure the images (e.g., `pacman.png`, `Blinky.png`, `Pinky.png`, etc.) and music (`pacman.mp3`) are in the correct folders (e.g., an `images` folder and at the proper level in the project directory) for the game to run correctly.
- If you want to modify or extend the ghosts' AI, the directional lists are centralized in the `directions.py` file.

## Contributing

Feel free to fork this project, suggest improvements, or fix bugs. All contributions are welcome!
>>>>>>> 49eee03 (Implement dynamic player image rotation based on movement direction)
