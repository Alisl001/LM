import tkinter as tk
from tkinter import messagebox 

class Piece:
    def __init__(self, piece_type, position):
        self.piece_type = piece_type  
        self.position = position 

    def __repr__(self):
        return f"{self.piece_type[0]}({self.position})"

    def copy(self):
        return Piece(self.piece_type, self.position)

class GameState:
    def __init__(self, board):
        self.board = board
        self.history = [board.copy()] 

    def display(self):
        self.board.display()

    def is_final_state(self):
        return self.board.is_final_state()

    def make_move(self, piece, new_position):
        new_board = self.board.copy()
        new_board.make_move(piece, new_position)
        new_state = GameState(new_board)
        self.history.append(new_board)  
        return new_state

class Board:
    def __init__(self, n, m, pieces, targets):
        self.n = n  
        self.m = m  
        self.grid = [[' ' for _ in range(m)] for _ in range(n)]
        self.pieces = {piece.position: piece for piece in pieces}  
        self.targets = targets 
        self.initial_pieces = pieces 
        self.initialize_board()

    def initialize_board(self):
        self.grid = [[' ' for _ in range(self.m)] for _ in range(self.n)]
        self.pieces = {piece.position: piece for piece in self.initial_pieces}  
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
        self.history_stack = [] 
        self.move_log = [] 
        
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

        # Solve using BFS Button
        self.solve_button = tk.Button(control_frame, text="Solve using BFS", command=self.solve_using_bfs, bd=5, font=("Calibri", 12, "bold"))
        self.solve_button.pack(pady=5)

        # Solve using DFS Button
        self.solve_dfs_button = tk.Button(control_frame, text="Solve using DFS", command=self.solve_using_dfs, bd=5, font=("Calibri", 12, "bold"))
        self.solve_dfs_button.pack(pady=5)


    def solve_using_dfs(self):
        solution_moves = dfs_solver(self.game_state)
        if solution_moves:
            messagebox.showinfo("Solution Found", "\n".join(solution_moves))
        else:
            messagebox.showinfo("No Solution", "No solution found using DFS.")
        self.reset_board()

    def solve_using_bfs(self):
        solution_moves = bfs_solver(self.game_state)
        if solution_moves:
            messagebox.showinfo("Solution Found", "\n".join(solution_moves))
        else:
            messagebox.showinfo("No Solution", "No solution found using BFS.")
        self.reset_board()

    def draw_board(self):
        self.canvas.delete("all")
        for row in range(self.game_state.board.n):
            for col in range(self.game_state.board.m):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = x1 + self.cell_size, y1 + self.cell_size
                color = "lightgreen" if (row, col) in self.game_state.board.targets else "white"
                
                if (row, col) == self.hover_cell:
                    color = "lightblue" 
                
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
        self.history_stack.clear()  
        self.clear_log()            
        self.game_state = GameState(self.initial_state.board.copy())
        self.draw_board()

    def undo_move(self):
        if self.history_stack:
            self.game_state = self.history_stack.pop()  
            self.remove_last_log_entry()  
            self.draw_board()
        else:
            messagebox.showinfo("Undo", "No more moves to undo!")

    def log_move(self, piece, new_position):
        # Move notation:
        piece_type = piece.piece_type[0]
        old_position = piece.position 
        log_entry = f"{piece_type}({old_position[0]}, {old_position[1]}) to ({new_position[0]}, {new_position[1]})\n"
        
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

# root = tk.Tk() 
# initial_pieces = [
#     Piece('Gray', (0, 1)), 
#     Piece('Gray', (1, 1)), 
#     Piece('Gray', (1, 2)), 
#     Piece('Red', (2, 3)), 
#     Piece('Purple', (2, 0))
#     ] 
# targets = [(0, 2), (1, 0), (1, 1), (2, 0), (2, 1)] 
# board = Board(3, 4, initial_pieces, targets) 
# game_state = GameState(board) 
# game_gui = GameGUI(root, game_state) 
# root.mainloop()


# root = tk.Tk()
# initial_pieces = [
#     Piece('Gray', (0, 1)), 
#     Piece('Gray', (0, 3)),
#     Piece('Purple', (0, 4))
# ]
# targets = [(0, 0), (0, 2), (0, 4)]
# board = Board(1, 5, initial_pieces, targets)
# game_state = GameState(board) 
# game_gui = GameGUI(root, game_state) 
# root.mainloop()

from collections import deque

def bfs_solver(initial_state):
    queue = deque([(initial_state, [])])  
    visited = set()  

    def state_key(state):
        return tuple((piece.position, piece.piece_type) for piece in state.board.pieces.values())

    visited.add(state_key(initial_state))

    while queue:
        current_state, moves = queue.popleft()

        if current_state.is_final_state():
            return moves

        for piece in current_state.board.pieces.values():
            if piece.piece_type in ['Red', 'Purple']:
                for new_position in generate_possible_moves(current_state.board, piece):
                    old_position = piece.position

                    new_state = current_state.make_move(piece, new_position)

                    new_state_key = state_key(new_state)
                    if new_state_key not in visited:
                        visited.add(new_state_key)
                        move_description = f"{piece.piece_type}({old_position[0]}, {old_position[1]}) to ({new_position[0]}, {new_position[1]})"
                        queue.append((new_state, moves + [move_description]))

    return None  

def generate_possible_moves(board, piece):
    possible_moves = []
    n, m = board.n, board.m  
    row, col = piece.position

    if piece.piece_type == 'Red':
        for r in range(n):
            for c in range(m):
                if board.can_move_to(r, c):
                    possible_moves.append((r, c))

    elif piece.piece_type == 'Purple':
        for r in range(n):
            for c in range(m):
                if board.can_move_to(r, c):
                    possible_moves.append((r, c))

    return possible_moves

def move_piece(state, piece, new_position):
    board_copy = [row[:] for row in state['board']]
    magnets_copy = [magnet.copy() for magnet in state['magnets']]
    
    old_row, old_col = piece['position']
    new_row, new_col = new_position
    
    board_copy[old_row][old_col] = ' '  
    board_copy[new_row][new_col] = piece['type'][0]  
    
    for magnet in magnets_copy:
        if magnet['position'] == (old_row, old_col):
            magnet['position'] = (new_row, new_col)
            break
    
    return {'board': board_copy, 'magnets': magnets_copy}


def dfs_solver(initial_state):
    stack = [(initial_state, [])] 
    visited = set() 

    def state_key(state):
        return tuple((piece.position, piece.piece_type) for piece in state.board.pieces.values())

    visited.add(state_key(initial_state))

    while stack:
        current_state, moves = stack.pop()

        if current_state.is_final_state():
            return moves

        for piece in current_state.board.pieces.values():
            if piece.piece_type in ['Red', 'Purple']:
                for new_position in generate_possible_moves(current_state.board, piece):
                    old_position = piece.position

                    new_state = current_state.make_move(piece, new_position)

                    new_state_key = state_key(new_state)
                    if new_state_key not in visited:
                        visited.add(new_state_key)
                        move_description = f"{piece.piece_type}({old_position[0]}, {old_position[1]}) to ({new_position[0]}, {new_position[1]})"
                        stack.append((new_state, moves + [move_description]))

    return None 

# initial_pieces = [
#     Piece('Gray', (0, 1)), 
#     Piece('Gray', (0, 3)),
#     Piece('Purple', (0, 4))
# ]
# targets = [(0, 0), (0, 2), (0, 4)]
# board = Board(1, 5, initial_pieces, targets)
# game_state = GameState(board)

# # Solve the game using BFS
# solution_moves = bfs_solver(game_state)

# if solution_moves:
#     print("Solution found:")
#     for move in solution_moves:
#         print(move)
# else:
#     print("No solution found")

root = tk.Tk()
initial_pieces = [
    Piece('Gray', (0, 1)), 
    Piece('Gray', (0, 3)),
    Piece('Purple', (0, 4))
]
targets = [(0, 0), (0, 2), (0, 4)]
board = Board(1, 5, initial_pieces, targets)
game_state = GameState(board)
game_gui = GameGUI(root, game_state)
root.mainloop()
