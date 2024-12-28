import pygame
from blobWars.constants import WIDTH, HEIGHT, WHITE, SQUARE_SIZE
from blobWars.game import Game

FPS = 15

WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Blob Wars')

def get_row_col_from_mouse(pos):
    x, y = pos
    row = y // SQUARE_SIZE
    col = x // SQUARE_SIZE
    return row, col

def main():
    run = True
    clock = pygame.time.Clock()
    game = Game(WIN)
    while run:
        clock.tick(FPS)
        winner = game.winner()
        if winner != 0:
            if winner == 1:
                print('blue is the winner')
            elif winner == -1:
                print('red is the winner')
            else:
                print('draw')
            game.reset()

        if game.turn == -1:
            game.ai_move()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = get_row_col_from_mouse(pos)
                game.select(row, col)
                game.update()

    pygame.quit()
main()
