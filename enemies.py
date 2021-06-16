"""
In this module are 3 classes that are able to collide with the player -> Block(wall), Point and of course Ghost
"""
import pygame
import random
from constant import *


class Block(pygame.sprite.Sprite):
    """
    Class of blocks that are inserted in place of the wall.
    """
    def __init__(self, pos, width, height):
        """
        Class constructor.
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.pos = pos
        self.rect = self.image.get_rect()
        self.rect.topleft = vector(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE))


class Point(pygame.sprite.Sprite):
    """
    Class of points.
    """
    def __init__(self, pos, color, width, height):
        """
        Class constructor.
        :param pos: vector position
        :param color: color of dot
        :param width: width
        :param height: height
        """
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)
        self.pos = pos
        pygame.draw.ellipse(self.image, color, [0, 0, width, height])
        self.rect = self.image.get_rect()
        self.rect.topleft = vector(int(self.pos.x * CELL_SIZE + 14), int(self.pos.y * CELL_SIZE + 14))


class Ghost(pygame.sprite.Sprite):
    """
    Class of ghosts
    """
    def __init__(self, pos, change_x, change_y, color):
        """
        Class constructor.
        :param pos: starting position vector
        :change_x: argument determine the horizontal direction of the movement
        :change_y: argument determine the vertical direction of the movement
        :param color: color of ghost
        """
        pygame.sprite.Sprite.__init__(self)
        self.change_x = change_x
        self.change_y = change_y
        self.pos = pos
        self.direction = None
        self.color = color
        self.velocity = VEL
        self.define_ghosts("right")
        self.rect = self.image.get_rect()
        self.rect.topleft = vector(int(self.pos.x * CELL_SIZE), int(self.pos.y * CELL_SIZE))

    def define_ghosts(self, direction):
        """
        Function determines the direction in which the ghost is moving and changes the image
        :param direction: (left or right)
        """
        if self.color == "pink":
            self.image = pygame.image.load(r"images/{}_ghost_{}.png".format(self.color, direction)).convert_alpha()
        elif self.color == "blue":
            self.image = pygame.image.load(r"images/{}_ghost_{}.png".format(self.color, direction)).convert_alpha()
        elif self.color == "green":
            self.image = pygame.image.load(r"images/{}_ghost_{}.png".format(self.color, direction)).convert_alpha()
        elif self.color == "orange":
            self.image = pygame.image.load(r"images/{}_ghost_{}.png".format(self.color, direction)).convert_alpha()
            self.image = pygame.transform.scale(self.image, CELL)

    def update(self):
        """
        Update movement.
        """
        self.rect.x += self.change_x
        self.rect.y += self.change_y
        if self.rect.right < 0:
            self.rect.left = SCREEN_WIDTH
        elif self.rect.left > SCREEN_WIDTH:
            self.rect.right = 0
        if self.rect.bottom < 0:
            self.rect.top = SCREEN_HEIGHT
        elif self.rect.top > SCREEN_HEIGHT:
            self.rect.bottom = 0

        self.check_way()

        if self.change_x == LEFT.x * self.velocity:
            self.define_ghosts("left")
        elif self.change_x == RIGHT.x * self.velocity:
            self.define_ghosts("right")
        else:
            pass

    def check_way(self):
        """
        Function randomly changes the direction of movement if the ghost is in the right place.
        """
        if self.rect.topleft in CROSS:
            self.direction = random.choice((LEFT, RIGHT, UP, DOWN))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in RIGHT_CORNER_DOWN:
            self.direction = random.choice((LEFT, UP))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in RIGHT_CORNER_UP:
            self.direction = random.choice((LEFT, DOWN))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in LEFT_CORNER_DOWN:
            self.direction = random.choice((RIGHT, UP))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in LEFT_CORNER_UP:
            self.direction = random.choice((RIGHT, DOWN))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in TRIANGLE_DOWN:
            self.direction = random.choice((LEFT, RIGHT, DOWN))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in TRIANGLE_UP:
            self.direction = random.choice((LEFT, RIGHT, UP))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in TRIANGLE_LEFT:
            self.direction = random.choice((LEFT, UP, DOWN))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
        if self.rect.topleft in TRIANGLE_RIGHT:
            self.direction = random.choice((RIGHT, UP, DOWN))
            self.change_x = self.direction.x * self.velocity
            self.change_y = self.direction.y * self.velocity
