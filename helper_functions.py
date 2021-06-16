import pygame
from constant import *


def add_score(file_name, text):
    best_file = open(file_name, 'a')
    best_file.write(text + "\n")
    best_file.close()


def get_best_score(file_name):
    try:

        best_file = open(file_name, 'r')
        lines = best_file.readlines()
        best_file.close()
        list_of_scores = [int(lines[i][:-1]) for i in range(0, len(lines))]
        list_of_scores.sort()

        return list_of_scores[-1]

    except FileNotFoundError:
        return "?"


def leaderboard_top(file_name):
    try:
        best_file = open(file_name, 'r')
        leaderboard = best_file.readlines()
        best_file.close()
        list_of_scores = [int(leaderboard[i][:-1]) for i in range(0, len(leaderboard))]
        list_of_scores.sort()
        list_of_scores.reverse()

        if len(leaderboard) < 9:
            return list_of_scores
        else:
            return list_of_scores[:9]

    except FileNotFoundError:
        return []


def leaderboard_update(screen, x, y, top_list, color):
    font = pygame.font.Font(ARCADE_FONT, 25)
    for i in top_list:
        title = font.render(str(i), True, color)
        screen.blit(title, (x + 50, y))
        y += 50


def draw_one_to_nine(screen, x, y, color):
    font = pygame.font.Font(ARCADE_FONT, 25)
    for i in range(9):
        number = font.render(str(i + 1) + ". ", True, color)
        screen.blit(number, (x, y))
        y += 50


def divide_long_text(text):
    return text.split("\n")


def text_update(screen, text):
    font = pygame.font.Font(ARCADE_FONT, 17)
    i = 0
    my_text = divide_long_text(text)
    for lin in my_text:
        dis_txt = font.render(lin, True, WHITE)
        width = dis_txt.get_width()
        height = dis_txt.get_height()
        pos_x = (SCREEN_WIDTH / 2) - (width / 2)
        pos_y = (SCREEN_HEIGHT / 2) - (height / 2) - 165
        screen.blit(dis_txt, (pos_x, pos_y + i))
        i += 60


def display_message(screen, message, size, place=1, color=RED):
    font = pygame.font.Font(ARCADE_FONT, int(size))
    label = font.render(message, True, color)
    width = label.get_width()
    height = label.get_height()
    posX = (SCREEN_WIDTH / 2) - (width / 2)
    posY = ((SCREEN_HEIGHT / 2) - (height / 2)) * place
    screen.blit(label, (posX, int(posY)))

# ================ DRAW BACKGROUND ================== #

def draw_up(screen, j, i):
    pygame.draw.line(screen, BLUE, [j * CELL_SIZE, i * CELL_SIZE], [(j + 1) * CELL_SIZE, i * CELL_SIZE], 3)


def draw_down(screen, j, i):
    pygame.draw.line(screen, BLUE, [j * CELL_SIZE, (i + 1) * CELL_SIZE], [(j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE], 3)


def draw_right(screen, j, i):
    pygame.draw.line(screen, BLUE, [(j + 1) * CELL_SIZE, i * CELL_SIZE], [(j + 1) * CELL_SIZE, (i + 1) * CELL_SIZE], 3)


def draw_left(screen, j, i):
    pygame.draw.line(screen, BLUE, [j * CELL_SIZE, i * CELL_SIZE], [j * CELL_SIZE, (i + 1) * CELL_SIZE], 3)


def draw_enviroment(screen):
    for i, row in enumerate(GRID):
        for j, item in enumerate(row):
            if item == 1:  # prosto poziomo linia
                draw_up(screen, j, i)  # gora
                draw_down(screen, j, i)  # dol
            elif item == 2:  # prosta poizomo linia
                draw_left(screen, j, i)  # lewo
                draw_right(screen, j, i)  # prawo
            elif item == 4:  # prawy dolny rog
                draw_down(screen, j, i)
                draw_right(screen, j, i)
            elif item == 5:  # lewy dolny rog
                draw_down(screen, j, i)
                draw_left(screen, j, i)
            elif item == 6:  # prawy gorny rog
                draw_up(screen, j, i)  # gora
                draw_right(screen, j, i)  # prawo
            elif item == 7:  # lewy gorny rog
                draw_up(screen, j, i)
                draw_left(screen, j, i)
            elif item == 'p':
                draw_left(screen, j, i)
            elif item == 'l':
                draw_right(screen, j, i)
            elif item == 'd':
                draw_up(screen, j, i)
            elif item == 'g':
                draw_down(screen, j, i)
