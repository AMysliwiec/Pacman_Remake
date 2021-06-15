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
        return "you are the first!"


def leaderboard_top(file_name):
    try:
        best_file = open(file_name, 'r')
        leaderboard = best_file.readlines()
        best_file.close()
        list_of_scores = [int(leaderboard[i][:-1]) for i in range(0, len(leaderboard))]
        list_of_scores.sort()
        list_of_scores.reverse()

        if len(leaderboard) < 5:
            return list_of_scores
        else:
            return list_of_scores[:5]

    except FileNotFoundError:
        return []


def leaderboard_update(screen, x, y, top_list):
    font = pygame.font.Font(None, 35)
    n = 1
    for i in top_list:
        title = font.render(str(n) + ".  " + str(i), True, GREEN)
        screen.blit(title, (x - 20, y))
        n += 1
        y += 30


def divide_long_text(text):
    return text.split("\n")


def text_update(screen, text):
    font = pygame.font.Font(None, 35)
    i = 0
    my_text = divide_long_text(text)
    for line in my_text:
        dis_txt = font.render(line, True, GREEN)
        screen.blit(dis_txt, (200, 200 + i))
        i += 30

