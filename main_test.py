import pygame
from game_test import Game
from helper_functions import *
from constant import *


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("PACMAN")
    icon = pygame.image.load('images/test.png')
    icon = pygame.transform.scale(icon, CELL)
    pygame.display.set_icon(icon)
    done = False
    clock = pygame.time.Clock()
    game = Game()
    # -------- Main Program Loop -----------
    while not done:
        done = game.process_events()
        game.run_logic()
        game.display_frame(screen)
        clock.tick(30)
    pygame.quit()


if __name__ == '__main__':
    main()
