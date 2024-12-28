import pygame
from .board import Board
from .constants import BLACK, WHITE, SQUARE_SIZE, BLUE, RED, ROWS, COLS, LEVEL
from copy import deepcopy
from blobWars.ai import AI

class Game:
    def __init__(self, win):
        self.win = win
        self._init()
        
    def _init(self):
        self.selected_row = None
        self.selected_col = None
        self.board = Board()
        self.turn = 1
        self.valid_moves_for_selected_piece = {}
        self.update()

    def update(self):
        self.board.draw(self.win)
        if self.selected_row is not None and self.selected_col is not None:
            self.draw_valid_moves()
        pygame.display.update()

    def reset(self):
        self._init()

    def select(self, row, col):
        if self.selected_row is not None and self.selected_col is not None:
            result = self._move(row, col)
            if not result:
                self.selected_row = None
                self.selected_col = None
                self.board.selected_row = None
                self.board.selected_col = None
                # self.select(row, col)
        piece = self.board.get_piece(row, col)
        if piece != 0 and piece != '#' and piece == self.turn:
            self.selected_row = row
            self.selected_col = col
            self.board.selected_row = row
            self.board.selected_col = col
            self.valid_moves_for_selected_piece = self.board.get_valid_moves(row, col)
            return True
        return False

    def _move(self, row, col):
        if self.selected_row is not None and self.selected_col is not None and (row, col) in self.valid_moves_for_selected_piece:
            self.board.move(self.selected_row, self.selected_col, row, col, self.valid_moves_for_selected_piece[(row, col)])
            
            self.change_turn()
        else:
            return False
        return True
    
    def change_turn(self):
        self.valid_moves_for_selected_piece = {}
        self.selected_row = None
        self.selected_col = None
        if self.turn == -1:
            self.turn = 1
        else:
            self.turn = -1

    def draw_valid_moves(self):
        for move in self.valid_moves_for_selected_piece:
            row, col = move
            if self.valid_moves_for_selected_piece[(row, col)] == 1:
                pygame.draw.circle(self.win, BLUE, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE  // 2), 15)
            elif self.valid_moves_for_selected_piece[(row, col)] == 2:
                pygame.draw.circle(self.win, RED, (col * SQUARE_SIZE + SQUARE_SIZE // 2, row * SQUARE_SIZE + SQUARE_SIZE  // 2), 15)

    def winner(self):
        return self.board.winner()

    def get_all_moves(self, board, player):
        boards = []
        for row in range(ROWS):
            for col in range(COLS):
                if board.board[row][col] == player:
                    moves = board.get_valid_moves(row, col)
                    for move in moves:
                        x, y = move
                        temp_board = deepcopy(board)
                        temp_board.move(row, col, x, y, moves[(x, y)])
                        boards.append(temp_board)
        return boards

    def ai_move(self):
        self.selected_row = None
        self.selected_col = None
        self.board.selected_row = None
        self.board.selected_col = None
        self.update()
        #TODO: Change the function here
        new_board = AI.random(self, self.board)
        self.board = new_board
        self.change_turn()
        self.update()
