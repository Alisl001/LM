# Logic Magnets Game  

## Overview

**Logic Magnets**  is a Python-based board game implemented using Tkinter for the GUI and incorporates algorithms like Breadth-First Search (BFS) and Depth-First Search (DFS) for solving game puzzles. The game consists of movable magnets with different effects on other pieces on a grid board. The goal is to position all magnets on their respective target locations.

### Game Pieces

1. **Red Magnets** : Can be moved and have a **pulling**  effect on other magnets in the same row and column.

2. **Purple Magnets** : Can be moved and have a **pushing**  effect on other magnets in the same row and column.

3. **Gray Magnets** : Are immovable but can be pushed or pulled by Red and Purple magnets.

### Objectives

- Move the magnets on the board to reach the designated target positions.

- Utilize BFS and DFS algorithms to find solutions automatically.

## Data Structures  

1.`Piece` Class
Represents each game piece with:

- **piece_type**  (`Red`, `Purple`, `Gray`)

- **position**  (row, column)

2.`Board` Class
Handles the board state:

- **n** : Number of rows.

- **m** : Number of columns.

- **pieces** : Dictionary mapping piece positions to their respective `Piece` objects.

- **targets** : List of target positions.

- **grid** : 2D list representing the board layout.

3.`GameState` Class
Tracks the current state of the game:

- **board** : An instance of the `Board` class.

- **history** : A list to store previous board states for undo functionality.

4.`GameGUI` Class
Implements the graphical user interface using Tkinter:

- Displays the board, handles mouse interactions, and provides control buttons (Reset, Undo, Solve).

## Algorithms

### Breadth-First Search (BFS)

The BFS algorithm is used to find the shortest sequence of moves to reach the final state.

#### BFS Data Structures

- **Queue (`deque`)** : Stores tuples of the current game state and the list of moves taken to reach it.

- **Visited Set** : Tracks visited states to avoid revisiting.

#### BFS Output

- Returns a list of moves if a solution is found.

- Returns `None` if no solution exists.

#### BFS Algorithm Explanation

1. Initialize the queue with the initial game state and an empty move list.

2. Use a set to store the unique state representations.

3. Dequeue an element, check if it's a final state.

4. If not, generate possible moves for each movable piece (Red or Purple).

5. Apply each move to generate a new state.

6. If the new state hasn't been visited, enqueue it with the updated move list.

7. Repeat until the queue is empty or a solution is found.

### Depth-First Search (DFS)  

The DFS algorithm explores possible moves to find a solution, prioritizing depth over breadth.

#### DFS Data Structures

- **Stack (List)** : Used instead of a queue to implement the LIFO principle of DFS.

- **Visited Set** : Tracks visited states to avoid cycles.

#### DFS Output

- Returns a list of moves if a solution is found.
  
- Returns `None` if no solution exists.

#### DFS Algorithm Explanation

1. Use a stack to store the game state and move list.

2. Check if the current state is the final state.

3. If not, generate possible moves for movable pieces.

4. Apply each move and check if the new state has been visited.

5. If not, push the new state onto the stack.

6. Continue exploring until a solution is found or the stack is empty.

### State Representation

Each board state is represented by a **tuple**  of pieces' positions and types:

```python
tuple((piece.position, piece.piece_type) for piece in state.board.pieces.values())
```

This representation ensures that states are uniquely identifiable, which is crucial for detecting repeated states in BFS and DFS algorithms.

## Features

### GUI Controls

- **Reset Board** : Resets the board to its initial state.

- **Undo Move** : Reverts to the previous game state.

- **Solve using BFS** : Automatically solves the puzzle using the BFS algorithm.

- **Solve using DFS** : Automatically solves the puzzle using the DFS algorithm.

- **Move Log** : Displays a history of moves made during the game.

### Example Notation for Moves

- **Red Magnet (R)** : `R(2, 3) to (2, 1)`

- **Purple Magnet (P)** : `P(1, 1) to (1, 3)`

### Game State Storage

- The `history_stack` in the GUI stores past game states for the Undo feature.

- Each move generates a new `GameState` object, which includes the updated board and history.
