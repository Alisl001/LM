import random

class AI:

    def random(game, board):
        if game.winner() != 0:
            return board
        moves = game.get_all_moves(board, -1)
        
        return random.choice(moves)
    
    #TODO: Your code
