import tkinter as tk
from tkinter import messagebox 

class Piece:
    def __init__(self, piece_type, position):
        self.piece_type = piece_type  # 'Gray', 'Red', or 'Purple'
        self.position = position  # (row, column)

    def __repr__(self):
        return f"{self.piece_type[0]}({self.position})"

    def copy(self):
        return Piece(self.piece_type, self.position)

class GameState:
    def __init__(self, board):
        self.board = board

    def display(self):
        self.board.display()

    def is_final_state(self):
        return self.board.is_final_state()

    def make_move(self, piece, new_position):
        new_board = self.board.copy()
        new_board.make_move(piece, new_position)
        return GameState(new_board)

class Board:
    def __init__(self, n, m, pieces, targets):
        self.n = n  # Number of rows
        self.m = m  # Number of columns
        self.grid = [[' ' for _ in range(m)] for _ in range(n)]
        self.pieces = {piece.position: piece for piece in pieces}  # Dict of pieces by their positions
        self.targets = targets 
        self.initial_pieces = pieces 
        self.initialize_board()

    def initialize_board(self):
        self.grid = [[' ' for _ in range(self.m)] for _ in range(self.n)]
        self.pieces = {piece.position: piece for piece in self.initial_pieces}  # Reset pieces
        for piece in self.pieces.values():
            row, col = piece.position
            self.grid[row][col] = piece.piece_type[0]
        for row, col in self.targets:
            if self.grid[row][col] == ' ':
                self.grid[row][col] = 'T'

    def display(self):
        for row in self.grid:
            print(" | ".join(row))
            print("-" * (self.m * 4 - 1))

    def can_move_to(self, row, col):
        return 0 <= row < self.n and 0 <= col < self.m and self.grid[row][col] in [' ', 'T']

    def move_red_magnet(self, piece, new_position):
        old_row, old_col = piece.position
        new_row, new_col = new_position
        if not self.can_move_to(new_row, new_col):
            print("Invalid move for Red magnet.")
            return

        self.grid[old_row][old_col] = ' '
        piece.position = new_position
        self.grid[new_row][new_col] = 'R'
        self.pieces[new_position] = piece
        del self.pieces[(old_row, old_col)]
        self._pull_magnets(new_row, new_col)

    def move_purple_magnet(self, piece, new_position):
        old_row, old_col = piece.position
        new_row, new_col = new_position
        if not self.can_move_to(new_row, new_col):
            print("Invalid move for Purple magnet.")
            return

        self.grid[old_row][old_col] = ' '
        piece.position = new_position
        self.grid[new_row][new_col] = 'P'
        self.pieces[new_position] = piece
        del self.pieces[(old_row, old_col)]
        self._push_magnets(new_row, new_col)

    def _shift_piece(self, row, col, row_offset, col_offset):
        new_row, new_col = row + row_offset, col + col_offset
        if self.can_move_to(new_row, new_col):
            self.grid[new_row][new_col] = self.grid[row][col]
            self.pieces[(new_row, new_col)] = self.pieces[(row, col)]
            self.pieces[(new_row, new_col)].position = (new_row, new_col)
            self.grid[row][col] = ' '
            del self.pieces[(row, col)]

    def _pull_magnets(self, row, col):
        for i in range(1, self.m):
            left = (row, col - i)
            if left in self.pieces and col - i + 1 < self.m:
                self._shift_piece(row, col - i, 0, 1)
            right = (row, col + i)
            if right in self.pieces and col + i - 1 >= 0:
                self._shift_piece(row, col + i, 0, -1)
        for i in range(1, self.n):
            up = (row - i, col)
            if up in self.pieces and row - i + 1 < self.n:
                self._shift_piece(row - i, col, 1, 0)
            down = (row + i, col)
            if down in self.pieces and row + i - 1 >= 0:
                self._shift_piece(row + i, col, -1, 0)

    def _push_magnets(self, row, col):
        for i in range(self.m - 1, 0, -1):
            left = (row, col - i)
            if left in self.pieces and col - i - 1 >= 0:
                self._shift_piece(row, col - i, 0, -1)
            right = (row, col + i)
            if right in self.pieces and col + i + 1 < self.m:
                self._shift_piece(row, col + i, 0, 1)
        for i in range(self.n - 1, 0, -1):
            up = (row - i, col)
            if up in self.pieces and row - i - 1 >= 0:
                self._shift_piece(row - i, col, -1, 0)
            down = (row + i, col)
            if down in self.pieces and row + i + 1 < self.n:
                self._shift_piece(row + i, col, 1, 0)

    def is_final_state(self):
        for piece in self.pieces.values():
            if piece.piece_type in ['Red', 'Purple', 'Gray'] and piece.position not in self.targets:
                return False
        return True

    def make_move(self, piece, new_position):
        if piece.piece_type == 'Red':
            self.move_red_magnet(piece, new_position)
        elif piece.piece_type == 'Purple':
            self.move_purple_magnet(piece, new_position)

    def copy(self):
        return Board(self.n, self.m, [piece.copy() for piece in self.pieces.values()], self.targets)

class GameGUI:
    def __init__(self, master, game_state):
        self.master = master
        self.master.title("Logic Magnets")
        self.game_state = game_state
        self.initial_state = GameState(game_state.board.copy())
        self.cell_size = 75
        self.history_stack = []  # Stack to keep track of game states for undo functionality
        self.move_log = []       # List to keep track of move log for display
        
        # Canvas and Board
        self.canvas = tk.Canvas(master, width=self.cell_size * self.game_state.board.m, height=self.cell_size * self.game_state.board.n)
        self.canvas.pack(side=tk.LEFT)
        self.selected_piece = None
        self.hover_cell = None
        self.draw_board()
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)
        
        # Control Frame
        control_frame = tk.Frame(master)
        control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10)
        
        # Reset Button
        self.reset_button = tk.Button(control_frame, text="Reset Board", command=self.reset_board, bd=5, font=("Calibri", 12, "bold"))
        self.reset_button.pack(pady=5)

        # Undo Button
        self.undo_button = tk.Button(control_frame, text="Undo", command=self.undo_move, bd=5, font=("Calibri", 12, "bold"))
        self.undo_button.pack(pady=5)

        # Move Log
        self.log_label = tk.Label(control_frame, text="Move Log:", font=("Calibri", 12, "bold"))
        self.log_label.pack(pady=5)
        self.move_log_text = tk.Text(control_frame, height=20, width=20, state='disabled', wrap='none')
        self.move_log_text.pack(pady=5)

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.game_state.board.n):
            for col in range(self.game_state.board.m):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "lightgreen" if (row, col) in self.game_state.board.targets else "white"
                
                if (row, col) == self.hover_cell:
                    color = "lightblue"  # Highlight hovered cell
                
                self.canvas.create_rectangle(x1, y1, x2, y2, fill=color, outline="black")

                if (row, col) in self.game_state.board.pieces:
                    piece = self.game_state.board.pieces[(row, col)]
                    piece_color = "gray" if piece.piece_type == 'Gray' else "red" if piece.piece_type == 'Red' else "purple"
                    shadow_offset = 3 if (row, col) != self.selected_piece else 0
                    self.canvas.create_oval(x1 + 10 + shadow_offset, y1 + 10 + shadow_offset,
                                            x2 - 10 + shadow_offset, y2 - 10 + shadow_offset,
                                            fill="black", outline="")
                    self.canvas.create_oval(x1 + 5, y1 + 5, x2 - 5, y2 - 5, fill=piece_color, outline="black", width=2)
                    if (row, col) == self.selected_piece:
                        self.canvas.create_rectangle(x1, y1, x2, y2, outline="blue", width=2)

    def on_click(self, event):
        row, col = event.y // self.cell_size, event.x // self.cell_size
        
        # Check if the clicked cell is the same as the currently selected piece
        if self.selected_piece == (row, col):
            self.selected_piece = None
        else:
            if self.selected_piece:
                piece = self.game_state.board.pieces.get(self.selected_piece)
                if piece and self.game_state.board.can_move_to(row, col):
                    self.history_stack.append(self.game_state)  # Push current state to history stack
                    self.log_move(piece, (row, col))            # Log the move
                    self.game_state = self.game_state.make_move(piece, (row, col))
                    self.selected_piece = None
                    if self.game_state.is_final_state():
                        self.draw_board()
                        self.show_win_message()
                self.draw_board()
            elif (row, col) in self.game_state.board.pieces:
                self.selected_piece = (row, col)
        self.draw_board()

    def on_hover(self, event):
        row, col = event.y // self.cell_size, event.x // self.cell_size
        if (row, col) != self.hover_cell:
            self.hover_cell = (row, col)
            self.draw_board()

    def show_win_message(self):
        messagebox.showinfo("Congratulations!", "You've won the game!")

    def reset_board(self):
        self.history_stack.clear()  # Clear history stack
        self.clear_log()            # Clear move log
        self.game_state = GameState(self.initial_state.board.copy())
        self.draw_board()

    def undo_move(self):
        if self.history_stack:
            self.game_state = self.history_stack.pop()  # Revert to previous state
            self.remove_last_log_entry()  # Remove last log entry
            self.draw_board()
        else:
            messagebox.showinfo("Undo", "No more moves to undo!")

    def log_move(self, piece, new_position):
        # Log the move notation
        piece_type = piece.piece_type[0]
        log_entry = f"{piece_type} to {new_position}\n"
        self.move_log_text.config(state='normal')
        self.move_log_text.insert('end', log_entry)
        self.move_log_text.config(state='disabled')

    def remove_last_log_entry(self):
        self.move_log_text.config(state='normal')
        self.move_log_text.delete("end-2l", "end-1l")
        self.move_log_text.config(state='disabled')

    def clear_log(self):
        self.move_log_text.config(state='normal')
        self.move_log_text.delete('1.0', tk.END)
        self.move_log_text.config(state='disabled')


root = tk.Tk() 
initial_pieces = [
    Piece('Gray', (0, 1)), 
    Piece('Gray', (1, 1)), 
    Piece('Gray', (1, 2)), 
    Piece('Red', (2, 3)), 
    Piece('Purple', (2, 0))
    ] 
targets = [(0, 2), (1, 0), (1, 1), (2, 0), (2, 1)] 
board = Board(3, 4, initial_pieces, targets) 
game_state = GameState(board) 
game_gui = GameGUI(root, game_state) 
root.mainloop()
