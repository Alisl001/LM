import pygame

WIDTH, HEIGHT = 800, 800
ROWS, COLS = 8, 8
SQUARE_SIZE = WIDTH//COLS
LEVEL = 1

#RGB
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128, 128, 128)

SQUARE_IMG = pygame.transform.scale(pygame.image.load('assets/square_brown_dark_1x.png'), (SQUARE_SIZE, SQUARE_SIZE))
EMPTY_SQUARE_IMG = pygame.transform.scale(pygame.image.load('assets/square gray dark _1x.png'), (SQUARE_SIZE, SQUARE_SIZE))

PLAYER_RED_IMG = pygame.transform.scale(pygame.image.load('assets/player_red.png'), (SQUARE_SIZE * 0.9, SQUARE_SIZE * 0.9))
PLAYER_RED_SELECTED_IMG = pygame.transform.scale(pygame.image.load('assets/player_red_selected.png'), (SQUARE_SIZE * 0.9, SQUARE_SIZE * 0.9))
PLAYER_BLUE_IMG = pygame.transform.scale(pygame.image.load('assets/player_blue.png'), (SQUARE_SIZE * 0.9, SQUARE_SIZE * 0.9))
PLAYER_BLUE_SELECTED_IMG = pygame.transform.scale(pygame.image.load('assets/player_blue_selected.png'), (SQUARE_SIZE * 0.9, SQUARE_SIZE * 0.9))




