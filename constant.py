"""
This file contains all constants used in the game code.
"""

import pygame

vector = pygame.math.Vector2

LEFT = vector(-1, 0)
RIGHT = vector(1, 0)
UP = vector(0, -1)
DOWN = vector(0, 1)
ZERO_VEC = vector(0, 0)

CELL_SIZE = 35
SCREEN_WIDTH = 19 * CELL_SIZE
SCREEN_HEIGHT = 21 * CELL_SIZE
CELL = (CELL_SIZE, CELL_SIZE)
VEL = 3
WALL_TOLERANCE = 5

TITLE_WIDTH = int(SCREEN_WIDTH / 4 * 3)
TITLE_HEIGHT = int(SCREEN_HEIGHT / 5)

GAME_OVER_WIDTH = int(SCREEN_WIDTH / 2)
GAME_OVER_HEIGHT = int(SCREEN_HEIGHT / 5)

ARROW_WIDTH = 150
ARROW_HEIGHT = 104

SCORE_FILE = "best_scores.txt"
SCORE_FILE_LVL2 = "best_scores_2.txt"

ARCADE_FONT = "ARCADE_R.TTF"

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
ORANGE_RED = (243, 43, 20)

# ======== STRINGS TO DISPLAY ON SCREEN ========== #

ABOUT = "HELLO THERE\n" \
        "MY NAME IS ALICJA\n" \
        "AND I CREATED THIS GAME\n" \
        "TO PERPETUATE THE FACT THAT\n" \
        "YOU CAN ALSO DO COOL THINGS\n" \
        "DURING YOUR STUDIES"

RULES = "EAT ALL OF THE DOTS \n" \
        "AND DON'T LET GHOST TO EAT YOU\n" \
        "- ON THE LEVEL 'EASY' \n" \
        "JUST CLICK THE ARROW \n" \
        "TO CHANGE DIRECTION\n" \
        "- ON THE HARD LEVEL \n" \
        "IT'S NOT THAT EASY ..."

EASY_MESSAGE = " \n" \
               " \n" \
               "DO YOU THINK THAT THIS RESULT\n" \
               "WILL BE SAVED AS THE BEST?\n" \
               " \n" \
               "TRY YOUR SKILLS AT 'HARD' LEVEL\n"

HARD_MESSAGE = " \n" \
                    "IMPRESSIVE...\n" \
                    "YOU MANAGED TO EAT EVERY DOT\n" \
                    "AND YOUR SCORE IS SO HIGH!\n" \
                    " \n" \
                    "LET THIS RESULT ALSO NOT BE SAVED\n" \
                    "SO THAT OTHERS ENJOY THE GAME TOO"

# ============= USEFUL STUFF ============= #

WALLS = []
LINES = []
RIGHT_CORNER_UP = []
RIGHT_CORNER_DOWN = []
LEFT_CORNER_UP = []
LEFT_CORNER_DOWN = []
CROSS = []
TRIANGLE_UP = []
TRIANGLE_DOWN = []
TRIANGLE_RIGHT = []
TRIANGLE_LEFT = []
CAN_GO = []

with open('walls.txt', 'r') as file:
    for y_index, line in enumerate(file):
        for x_index, char in enumerate(line):
            if char == 'P':
                PACMAN_PLACE = vector(x_index, y_index)
            if char == 'P' or char == '1' or char == '3' or char == '4' or char == '5' or char == '6' or \
                    char == '7' or char == 'p' or char == 'g' or char == 'd' or char == 'l':
                CAN_GO.append(vector(x_index, y_index))
            if char == '0':
                WALLS.append(vector(x_index, y_index))
            if char == '1':
                LINES.append(vector(x_index, y_index))
            if char == '3':
                CROSS.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == '4':
                RIGHT_CORNER_DOWN.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == '5':
                LEFT_CORNER_DOWN.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == '6':
                RIGHT_CORNER_UP.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == '7':
                LEFT_CORNER_UP.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == 'p':
                TRIANGLE_RIGHT.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == 'l':
                TRIANGLE_LEFT.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == 'g':
                TRIANGLE_UP.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))
            if char == 'd':
                TRIANGLE_DOWN.append(vector(x_index * CELL_SIZE, y_index * CELL_SIZE))

GRID = ((0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0),
        (0, 7, 1, 1, 'd', 1, 1, 1, 6, 0, 7, 1, 1, 1, 'd', 1, 1, 6, 0),
        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
        (0, 'p', 1, 1, 3, 1, 'd', 1, 'g', 1, 'g', 1, 'd', 1, 3, 1, 1, 'l', 0),
        (0, 2, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 2, 0),
        (0, 5, 1, 1, 'l', 0, 5, 1, 6, 0, 7, 1, 4, 0, 'p', 1, 1, 4, 0),
        (0, 0, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 0, 0),
        (0, 0, 0, 0, 2, 0, 7, 1, 'g', 1, 'g', 1, 6, 0, 2, 0, 0, 0, 0),
        (0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0),
        (1, 1, 1, 1, 3, 1, 'l', 0, 0, 0, 0, 0, 'p', 1, 3, 1, 1, 1, 1),
        (0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0),
        (0, 0, 0, 0, 2, 0, 'p', 1, 1, 1, 1, 1, 'l', 0, 2, 0, 0, 0, 0),
        (0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0),
        (0, 7, 1, 1, 3, 1, 'g', 1, 6, 0, 7, 1, 'g', 1, 3, 1, 1, 6, 0),
        (0, 2, 0, 0, 2, 0, 0, 0, 2, 0, 2, 0, 0, 0, 2, 0, 0, 2, 0),
        (0, 5, 6, 0, 'p', 1, 'd', 1, 'g', 1, 'g', 1, 'd', 1, 'l', 0, 7, 4, 0),
        (0, 0, 2, 0, 2, 0, 2, 0, 0, 0, 0, 0, 2, 0, 2, 0, 2, 0, 0),
        (0, 7, 'g', 1, 4, 0, 5, 1, 6, 0, 7, 1, 4, 0, 5, 1, 'g', 6, 0),
        (0, 2, 0, 0, 0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0, 0, 0, 2, 0),
        (0, 5, 1, 1, 1, 1, 1, 1, 'g', 1, 'g', 1, 1, 1, 1, 1, 1, 4, 0),
        (0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))
