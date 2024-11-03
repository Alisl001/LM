# Logic Magnets Game 
This project implements the **Logic Magnets**  game in Python, with a GUI built using tkinter. The game logic and GUI are structured into classes that manage game states, board rendering, and user interactions. Below is an overview of the code structure, classes, and main methods.

## Code Structure 

The code is organized into the following classes:
 
- **Piece** : Represents individual game pieces with type and position.
 
- **GameState** : Tracks the current game state, including the board layout and move history.
 
- **Board** : Manages the grid, pieces, targets, and core game logic, including move validation and the pull/push effects of magnets.
 
- **GameGUI** : Handles the graphical interface, allowing users to interact with the game through mouse clicks and buttons for resetting the board and undoing moves.

## Class Overview 

`Piece`
Defines each game piece with:
 
- `piece_type`: Type of magnet (Red, Purple, or Gray).
 
- `position`: Current position on the board.


`GameState`
Tracks the game progression:
 
- `board`: The board's current layout.
 
- `history`: Stores board states for undo functionality.
 
- `make_move(piece, new_position)`: Updates game state with a new move.


`Board`
Handles game logic, board setup, and magnet effects:
 
- `initialize_board()`: Sets up the initial board grid with pieces and targets.
 
- `can_move_to(row, col)`: Checks if a piece can move to a specified position.
 
- `move_red_magnet(piece, new_position)`: Moves Red magnets and applies a pull effect on nearby magnets.
 
- `move_purple_magnet(piece, new_position)`: Moves Purple magnets and applies a push effect on nearby magnets.
 
- `is_final_state()`: Checks if all pieces are in their target positions.
 
- `copy()`: Creates a copy of the board for tracking state changes.


`GameGUI`
Manages the graphical interface and user interactions:
 
- `draw_board()`: Renders the board and pieces.
 
- `on_click(event)`: Handles piece selection and movement.
 
- `reset_board()`: Resets the game to its initial state.
 
- `undo_move()`: Reverts to the previous game state.
 
- `log_move(piece, new_position)`: Logs each move in the move log display.


## Usage 

1. Run the code to launch the game interface.

2. Use the GUI to select and move pieces by clicking.

3. View move history in the move log, reset the board, or undo moves.

## Example Output 

Here’s a sample layout with Red, Purple, and Gray magnets on a 3x4 board:

![Alt text](images/Puzzle%20Example.png "Puzzle Example")
![Alt text](images/Puzzle%20Win.png "Puzzle Win")

This structure supports expansion, making it adaptable for additional features and algorithms.