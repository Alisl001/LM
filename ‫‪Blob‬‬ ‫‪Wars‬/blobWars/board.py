from .constants import ROWS, COLS, SQUARE_SIZE, BLACK, SQUARE_IMG, EMPTY_SQUARE_IMG, PLAYER_RED_IMG, PLAYER_RED_SELECTED_IMG, PLAYER_BLUE_IMG, PLAYER_BLUE_SELECTED_IMG

class Board:
    def __init__(self):
        self.board = []
        self.create_boared()
        self.selected_row = None
        self.selected_col = None

    def create_boared(self):
        self.board = [
                    [1, 0, 0, 0, 0, 0, 0, 1],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, '#', '#', 0, 0, 0],
                    [0, 0, 0, '#', '#', 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0],
                    [-1, 0, 0, 0, 0, 0, 0, -1],
                ]

    def draw_squares(self, win):
        win.fill(BLACK)
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != '#':
                    win.blit(SQUARE_IMG, (row * SQUARE_SIZE, col * SQUARE_SIZE))
                else:
                    win.blit(EMPTY_SQUARE_IMG, (row * SQUARE_SIZE, col * SQUARE_SIZE))

    def move(self, old_row, old_col, new_row, new_col, moveType):
        if self.board[new_row][new_col] == 0:
            self.board[new_row][new_col] = self.board[old_row][old_col]
            if moveType == 2:
                self.board[old_row][old_col] = 0
            for i in range(-1, 2):
                for j in range(-1, 2):
                    if 0 <= new_row + i < ROWS and 0 <= new_col + j < COLS:
                        if self.board[new_row + i][new_col + j] != 0 and self.board[new_row + i][new_col + j] != '#':
                            self.board[new_row + i][new_col + j] = self.board[new_row][new_col]

    def get_piece(self, row, col):
        if row >= ROWS or row < 0 or col >= COLS or col < 0:
            return 0
        return self.board[row][col]

    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0 and piece != '#':
                    x = SQUARE_SIZE * col + SQUARE_SIZE // 2
                    y = SQUARE_SIZE * row + SQUARE_SIZE // 2
                    if piece == 1:
                        if row == self.selected_row and col == self.selected_col:
                            img = PLAYER_BLUE_SELECTED_IMG
                        else:
                            img = PLAYER_BLUE_IMG
                    elif piece == -1:
                        if row == self.selected_row and col == self.selected_col:
                            img = PLAYER_RED_SELECTED_IMG
                        else:
                            img = PLAYER_RED_IMG
                    if img:
                        win.blit(img, (x - img.get_width()//2, y - img.get_height()//2))

    def get_valid_moves(self, row, col):
        moves = {}
        for i in range(-1, 2):
            for j in range(-1, 2):
                if 0 <= row + i < ROWS and 0 <= col + j < COLS:
                    if self.board[row + i][col + j] == 0:
                        moves[(row + i, col + j)] = 1
        for i in range(-2, 3):
            for j in range(-2, 3):
                if 0 <= row + i < ROWS and 0 <= col + j < COLS and (row + i, col + j) not in moves:
                    if self.board[row + i][col + j] == 0:
                        moves[(row + i, col + j)] = 2
        return moves

    def winner(self):
        redFfownd = False
        blueFownd = False
        emptyFownd = False
        sum = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] == -1:
                    redFfownd = True
                if self.board[row][col] == 1:
                    blueFownd = True
                if self.board[row][col] == 0:
                    emptyFownd = True
                if self.board[row][col] != '#':
                    sum += self.board[row][col]
        if not redFfownd:
            return 1
        if not blueFownd:
            return -1
        if not emptyFownd:
            if sum > 0:
                return 1
            elif sum < 0:
                return -1
            else:
                return 'draw'
        return 0

    def evaluate(self):
        sum = 0
        for row in range(ROWS):
            for col in range(COLS):
                if self.board[row][col] != '#':
                    sum += self.board[row][col]
        return sum


