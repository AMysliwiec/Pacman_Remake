import pygame
from player_test import Player
from enemies_test import *
from helper_functions import *
from constant import *


class Game(object):
    score = -1
    lives = 3

    dots_group = pygame.sprite.Group()
    for place in CAN_GO:
        dots_group.add(Point(place, WHITE, 8, 8))

    level = "easy"


    def __init__(self):
        self.font = pygame.font.Font(None, 40)
        self.about = False
        self.best = False
        self.game_over = True

        # Create the font for displaying the score on the screen
        self.font = pygame.font.Font(None, 35)
        self.menu = Menu(("Easy LVL", "Less Easy LVL", "About", "Best scores", "Exit"), font_color=WHITE, font_size=60)
        self.player = Player(PACMAN_PLACE, "images/start.png")
        self.walls = pygame.sprite.Group()
        for wall in WALLS:
            self.walls.add(Block(wall, CELL_SIZE, CELL_SIZE))
        self.enemies = pygame.sprite.Group()
        self.ghost1 = Ghost(vector(9, 19), 3, 0, "pink")
        self.ghost2 = Ghost(vector(17, 2), 0, -3, "blue")
        self.ghost3 = Ghost(vector(1, 1), 0, 3, "green")
        if self.level == "less_easy":
            self.ghost1 = Ghost(vector(1, 18), 0, -3, "pink")
            self.ghost4 = Ghost(vector(17, 17), 0, -3, "orange")
        self.ghost_list = [self.ghost1, self.ghost2, self.ghost3]
        if self.level == "less_easy":
            self.ghost_list.append(self.ghost4)
            for ghost in self.ghost_list:
                ghost.velocity = VEL * 2

        for ghost in self.ghost_list:
            self.enemies.add(ghost)

        self.pacman_sound = pygame.mixer.Sound("sounds/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("sounds/game_over_sound.ogg")
        self.hit_sound = pygame.mixer.Sound("sounds/hit_sound.ogg")

    def process_events(self):
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                return True
            self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if self.game_over and not self.about:
                        if self.menu.state == 0:
                            # ---- START ------
                            self.level = "easy"
                            self.score = -1
                            self.lives = 3
                            self.dots_group.empty()
                            for place in CAN_GO:
                                self.dots_group.add(Point(place, WHITE, 8, 8))
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 1:
                            self.level = "less_easy"
                            self.score = -1
                            self.lives = 2
                            self.dots_group.empty()
                            for place in CAN_GO:
                                self.dots_group.add(Point(place, WHITE, 8, 8))
                            self.__init__()
                            self.game_over = False
                        elif self.menu.state == 2:
                            # --- ABOUT ------
                            self.about = True
                        elif self.menu.state == 3:
                            # --- LEADERBOARD ------
                            self.best = True
                        elif self.menu.state == 4:
                            # --- EXIT -------
                            # User clicked exit
                            return True

                elif event.key == pygame.K_RIGHT:
                    self.player.move_right()

                elif event.key == pygame.K_LEFT:
                    self.player.move_left()

                elif event.key == pygame.K_UP:
                    self.player.move_up()

                elif event.key == pygame.K_DOWN:
                    self.player.move_down()

                elif event.key == pygame.K_ESCAPE:
                    self.game_over = True
                    self.about = False
                    self.best = False

            if self.level == "less_easy":
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_RIGHT:
                        self.player.stop_move_right()
                    elif event.key == pygame.K_LEFT:
                        self.player.stop_move_left()
                    elif event.key == pygame.K_UP:
                        self.player.stop_move_up()
                    elif event.key == pygame.K_DOWN:
                        self.player.stop_move_down()

        return False


    def run_logic(self):
        if not self.game_over:
            self.player.update()
            block_hit_list = pygame.sprite.spritecollide(self.player, self.dots_group, True)
            if len(block_hit_list) > 0:
                self.pacman_sound.play()
                self.score += 1

            block_hit_list = pygame.sprite.spritecollide(self.player, self.walls, False)
            if len(block_hit_list) > 0:
                for wall in block_hit_list:
                    if self.player.change_x > 0:
                        self.player.rect.right = wall.rect.left - WALL_TOLERANCE
                        self.player.change_x = 0
                    elif self.player.change_x < 0:
                        self.player.rect.left = wall.rect.right + WALL_TOLERANCE
                        self.player.change_x = 0

                    if self.player.change_y > 0:
                        self.player.rect.bottom = wall.rect.top - WALL_TOLERANCE
                        self.player.change_y = 0
                    elif self.player.change_y < 0:
                        self.player.rect.top = wall.rect.bottom + WALL_TOLERANCE
                        self.player.change_y = 0

            self.enemies.update()
            """ghost_list = [self.ghost1, self.ghost2, self.ghost3]
            if self.level == "less_easy":
                ghost_list.append(self.ghost4)"""

            for ghost in self.ghost_list:
                block_hit_list = pygame.sprite.spritecollide(ghost, self.walls, False)
                if len(block_hit_list) > 0:
                    for wall in block_hit_list:
                        if ghost.change_x > 0:
                            ghost.rect.right = wall.rect.left
                            ghost.change_x = 0
                        elif ghost.change_x < 0:
                            ghost.rect.left = wall.rect.right
                            ghost.change_x = 0

                        if ghost.change_y > 0:
                            ghost.rect.bottom = wall.rect.top
                            ghost.change_y = 0
                        elif ghost.change_y < 0:
                            ghost.rect.top = wall.rect.bottom
                            ghost.change_y = 0

            block_hit_list = pygame.sprite.spritecollide(self.player, self.enemies, True)
            if len(block_hit_list) > 0:
                self.lives -= 1
                if self.lives > 0:
                    self.hit_sound.play()
                    self.__init__()
                else:
                    self.player.explosion = True
                    self.game_over_sound.play()
                    add_score(SCORE_FILE, str(self.score))

            self.game_over = self.player.game_over
            # self.enemies.update()

    def display_frame(self, screen):
        screen.fill(BLACK)
        # --- Drawing code should go here
        if self.game_over:
            if self.about:
                text = "siema\nto moja gra\njest zajebista"
                text_update(screen, text)
            elif self.best:
                self.display_message(screen, "TOP 10 SCORES", 1/4)
                leaderboard_update(screen, 200, 200, leaderboard_top(SCORE_FILE))
            else:
                self.menu.display_frame(screen)
        else:
            # --- Draw the game here ---
            self.walls.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            text = self.font.render("Score: " + str(self.score), True, RED)
            lives_text = self.font.render("Lives: " + str(self.lives), True, RED)
            best_score = get_best_score(SCORE_FILE)
            best_score_text = self.font.render("Best score: " + str(best_score), True, RED)
            screen.blit(text, [100, 8])
            screen.blit(lives_text, [300, 8])  # tekst alternatywny do zdjec
            screen.blit(best_score_text, [500, 8])

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

    def display_message(self, screen, message, place = 1, color=RED):
        label = self.font.render(message, True, color)
        # Get the width and height of the label
        width = label.get_width()
        height = label.get_height()
        # Determine the position of the label
        posX = (SCREEN_WIDTH / 2) - (width / 2)
        posY = ((SCREEN_HEIGHT / 2) - (height / 2)) * place
        # Draw the label onto the screen
        screen.blit(label, (posX, posY))


class Menu(object):
    state = 0

    def __init__(self, items, font_color=BLACK, select_color=GREEN, ttf_font=None, font_size=25):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)
        self.title = pygame.image.load("images/tytul.jpg").convert_alpha()
        self.title = pygame.transform.scale(self.title, (TITLE_WIDTH, TITLE_HEIGHT))

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            pos_x = (SCREEN_WIDTH / 2) - (width / 2)
            pos_y = (SCREEN_HEIGHT / 2) - (len(self.items) * height / 2) + (index * height)
            pos_title_x = (SCREEN_WIDTH / 2) - (TITLE_WIDTH / 2)
            pos_title_y = TITLE_HEIGHT / 2

            screen.blit(label, (pos_x, pos_y))
            screen.blit(self.title, (pos_title_x, pos_title_y))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
