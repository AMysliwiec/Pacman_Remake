import pygame
from constant import *


class Player(pygame.sprite.Sprite):
    change_x = ZERO_VEC.x
    change_y = ZERO_VEC.y
    explosion = False
    game_over = False
    death = False

    def __init__(self, pos, filename):

        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(filename).convert_alpha()
        self.image = pygame.transform.scale(self.image, (30, 30))
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.pos = pos
        self.rect.topleft = vector(self.pos.x * CELL_SIZE, self.pos.y * CELL_SIZE)

        img = pygame.image.load("images/chodzenie.png").convert_alpha()
        img_down = pygame.image.load("images/walk_down.png").convert_alpha()
        img_up = pygame.image.load("images/pacman_back.png").convert_alpha()

        self.move_right_animation = Animation(img, CELL_SIZE, CELL_SIZE)
        self.move_left_animation = Animation(pygame.transform.flip(img, True, False), CELL_SIZE, CELL_SIZE)
        self.move_up_animation = Animation(img_up, CELL_SIZE, CELL_SIZE)
        self.move_down_animation = Animation(img_down, CELL_SIZE, CELL_SIZE)

        img = pygame.image.load("images/ded.png").convert_alpha()
        self.explosion_animation = Animation(img, CELL_SIZE, CELL_SIZE)

        self.player_image = pygame.image.load(filename).convert_alpha()
        self.player_image.set_colorkey(BLACK)

    def update(self):
        if not self.explosion:
            if self.rect.right < 0:
                self.rect.left = SCREEN_WIDTH
            elif self.rect.left > SCREEN_WIDTH:
                self.rect.right = 0
            if self.rect.bottom < 0:
                self.rect.top = SCREEN_HEIGHT
            elif self.rect.top > SCREEN_HEIGHT:
                self.rect.bottom = 0

            self.rect.x += self.change_x
            self.rect.y += self.change_y

            if self.change_x > 0:
                self.move_right_animation.update(5)
                self.image = self.move_right_animation.get_current_image()
            elif self.change_x < 0:
                self.move_left_animation.update(5)
                self.image = self.move_left_animation.get_current_image()

            if self.change_y > 0:
                self.move_down_animation.update(5)
                self.image = self.move_down_animation.get_current_image()
            elif self.change_y < 0:
                self.move_up_animation.update(5)
                self.image = self.move_up_animation.get_current_image()
        else:
            if self.explosion_animation.index == self.explosion_animation.get_length() - 1:
                pygame.time.wait(500)
                self.game_over = True
                self.death = True
            self.explosion_animation.update(6)
            self.image = self.explosion_animation.get_current_image()

    def move_right(self):
        self.change_x = RIGHT.x * VEL
        self.change_y = RIGHT.y * VEL

    def move_left(self):
        self.change_x = LEFT.x * VEL
        self.change_y = LEFT.y * VEL

    def move_up(self):
        self.change_x = UP.x * VEL
        self.change_y = UP.y * VEL

    def move_down(self):
        self.change_x = DOWN.x * VEL
        self.change_y = DOWN.y * VEL

    def stop_move_right(self):
        if self.change_x != ZERO_VEC.x:
            self.image = self.player_image
        self.change_x = ZERO_VEC.x

    def stop_move_left(self):
        if self.change_x != ZERO_VEC.x:
            self.image = pygame.transform.flip(self.player_image, True, False)
        self.change_x = ZERO_VEC.x

    def stop_move_up(self):
        if self.change_y != ZERO_VEC.y:
            self.image = self.move_up_animation.get_current_image()
        self.change_y = ZERO_VEC.y

    def stop_move_down(self):
        if self.change_y != ZERO_VEC.y:
            self.image = self.move_down_animation.get_current_image()
        self.change_y = ZERO_VEC.y


class Animation(object):
    def __init__(self, img, width, height):
        self.sprite_sheet = img
        self.image_list = []
        self.load_images(width, height)
        self.index = 0
        self.clock = 1

    def load_images(self, width, height):
        for y in range(0, self.sprite_sheet.get_height(), height):
            for x in range(0, self.sprite_sheet.get_width(), width):
                img = self.get_image(x, y, width, height)
                self.image_list.append(img)

    def get_image(self, x, y, width, height):
        image = pygame.Surface([width, height]).convert()
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        image.set_colorkey(BLACK)
        return image

    def get_current_image(self):
        return self.image_list[self.index]

    def get_length(self):
        return len(self.image_list)

    def update(self, fps=30):
        step = 30 // fps
        l = range(1, 30, step)
        if self.clock == 30:
            self.clock = 1
        else:
            self.clock += 1

        if self.clock in l:
            self.index += 1
            if self.index == len(self.image_list):
                self.index = 0
