# py2048

`py2048` is a Python package that implements the core game logic for the popular 2048 puzzle game. This package provides a `GameEngine` class that handles board operations, tile generation, movement, and game state management.

## Description

This package focuses solely on the backend game logic, making it suitable for integration into various frontends (e.g., console-based, GUI, web).

## Installation

To install `py2048`, you can use pip:

```bash
pip install py2048
```

Alternatively, if you have cloned the repository, you can install it from the local directory:

```bash
pip install .
```

## Usage

Here's a basic example of how to use the `GameEngine`:

```python
from main import GameEngine

# Initialize the game with a 4x4 board
game = GameEngine(size=4)

print("Initial Board:")
for row in game.board:
    print(row)
print(f"Score: {game.score}")

# Make a move (e.g., 'left', 'right', 'up', 'down')
game.move("left")

print("\nBoard after 'left' move:")
for row in game.board:
    print(row)
print(f"Score: {game.score}")

# Check if the game is over
if game.is_game_over():
    print("\nGame Over!")
else:
    print("\nGame continues...")
```

## GameEngine Class

The `GameEngine` class provides the following key methods:

- `__init__(self, size: int = 4)`: Initializes the game board.
- `get_empty_cells(self) -> List[Tuple[int, int]]`: Returns a list of empty cell coordinates.
- `add_tile(self)`: Adds a new 2 or 4 tile to a random empty cell.
- `move(self, direction: str)`: Moves tiles in the specified direction ('up', 'down', 'left', 'right') and merges them.
- `is_game_over(self) -> bool`: Checks if there are no more possible moves.
- `score`: The current score of the game.

## Author

Sheikh Hafijul Ali
mail@hafijul.dev
