import pygame
from player import Player
from enemies import *
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
        self.rules = False
        self.best = False
        self.game_over = True
        self.game_over_screen = False
        self.end_easy = False
        self.end_medium = False

        self.font = pygame.font.Font(ARCADE_FONT, 15)
        self.menu = Menu(("Easy LVL", "Medium LVL", "How to play", "About", "Best scores", "Exit"),
                         font_color=WHITE, font_size=30)
        self.player = Player(PACMAN_PLACE, "images/start.png")

        self.walls = pygame.sprite.Group()
        for wall in WALLS:
            self.walls.add(Block(wall, CELL_SIZE, CELL_SIZE))

        self.enemies = pygame.sprite.Group()
        self.ghost1 = Ghost(vector(9, 19), 3, 0, "pink")
        self.ghost2 = Ghost(vector(17, 2), 0, -3, "blue")
        self.ghost3 = Ghost(vector(1, 1), 0, 3, "green")

        if self.level == "medium":
            self.ghost1 = Ghost(vector(1, 18), 0, -3, "pink")
            self.ghost4 = Ghost(vector(17, 17), 0, -3, "orange")

        self.ghost_list = [self.ghost1, self.ghost2, self.ghost3]

        if self.level == "medium":
            self.ghost_list.append(self.ghost4)
            for ghost in self.ghost_list:
                ghost.velocity = VEL * 2

        for ghost in self.ghost_list:
            self.enemies.add(ghost)

        self.pacman_sound = pygame.mixer.Sound("sounds/pacman_sound.ogg")
        self.game_over_sound = pygame.mixer.Sound("sounds/game_over_sound.ogg")
        self.hit_sound = pygame.mixer.Sound("sounds/hit_sound.ogg")
        self.hello = pygame.mixer.Sound("sounds/obi-wan-hello-there.mp3")
        self.win = pygame.mixer.Sound("sounds/pac-man-intermission.mp3")

    def process_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if self.game_over and not self.about and not self.game_over_screen \
                    and not self.rules and not self.best and not self.end_medium and not self.end_easy:
                self.menu.event_handler(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:

                    if self.game_over and not self.about and not self.game_over_screen \
                            and not self.rules and not self.best and not self.end_medium and not self.end_easy:

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
                            self.level = "medium"
                            self.score = -1
                            self.lives = 1
                            self.dots_group.empty()
                            for place in CAN_GO:
                                self.dots_group.add(Point(place, WHITE, 8, 8))
                            self.__init__()
                            self.game_over = False

                        elif self.menu.state == 2:
                            # --- HOW TO PLAY ------
                            self.rules = True

                        elif self.menu.state == 3:
                            # --- ABOUT ------
                            self.hello.play()
                            self.about = True

                        elif self.menu.state == 4:
                            # --- LEADERBOARD ------
                            self.best = True

                        elif self.menu.state == 5:
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
                    self.pacman_sound.play()
                    self.win.stop()
                    self.game_over = True
                    self.about = False
                    self.best = False
                    self.rules = False
                    self.game_over_screen = False
                    self.end_easy = False
                    self.end_medium = False

            if self.level == "medium":
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
                    if self.level == "easy":
                        add_score(SCORE_FILE, str(self.score))
                    else:
                        add_score(SCORE_FILE_LVL2, str(self.score))

            self.game_over = self.player.game_over
            self.game_over_screen = self.player.death
            if not self.dots_group:
            # if len(self.dots_group.sprites()) == 180:
                self.win.play()
                self.game_over = True
                if self.level == "easy":
                    self.end_easy = True
                else:
                    self.end_medium = True

# ========================= DRAW THE GAME =============================== #

    def display_frame(self, screen):
        screen.fill(BLACK)
        if self.game_over:
            if self.about:
                obi = pygame.image.load("images/obi_wan.png").convert_alpha()
                obi = pygame.transform.rotate(obi, 270)
                screen.blit(obi, (0, 50))
                text_update(screen, ABOUT)
                display_message(screen, "Press ESC to back to the main menu", 15, 1.9, ORANGE_RED)
            elif self.game_over_screen:
                pic = pygame.image.load("images/game_over_pic.jpg").convert_alpha()
                pic = pygame.transform.scale(pic, (GAME_OVER_WIDTH, GAME_OVER_HEIGHT))
                pos_title_x = (SCREEN_WIDTH / 2) - (GAME_OVER_WIDTH / 2)
                pos_title_y = GAME_OVER_HEIGHT / 2
                screen.blit(pic, (pos_title_x, pos_title_y))

                display_message(screen, "Your score: {}".format(self.score), 25, 1, GREEN)
                display_message(screen, "Press ESC to back to the main menu", 15, 1.9, ORANGE_RED)

            elif self.end_medium:
                display_message(screen, "YOU WIN!", 40, 0.25, ORANGE_RED)
                text_update(screen, MEDIUM_MESSAGE)
                display_message(screen, "Press ESC to back to the main menu", 15, 1.9, ORANGE_RED)

            elif self.end_easy:
                display_message(screen, "YOU ... WIN?", 40, 0.25, ORANGE_RED)
                text_update(screen, EASY_MESSAGE)
                display_message(screen, "Press ESC to back to the main menu", 15, 1.9, ORANGE_RED)

            elif self.rules:
                pic = pygame.image.load("images/arrow_keys.png").convert_alpha()
                screen.blit(pic, (130, 40))
                display_message(screen, "Use            to move the PACMAN", 17, 0.25, WHITE)
                text_update(screen, RULES)
                display_message(screen, "Press ESC to back to the main menu", 15, 1.9, ORANGE_RED)

            elif self.best:
                display_message(screen, "TOP 9 SCORES", 35, 0.2)
                display_message(screen, "EASY          MEDIUM", 20, 0.4, WHITE)
                draw_one_to_nine(screen, 125, 200, GREEN)
                leaderboard_update(screen, 125, 200, leaderboard_top(SCORE_FILE), GREEN)
                draw_one_to_nine(screen, 420, 200, YELLOW)
                leaderboard_update(screen, 420, 200, leaderboard_top(SCORE_FILE_LVL2), YELLOW)
                display_message(screen, "Press ESC to back to the main menu", 15, 1.9, ORANGE_RED)
            else:
                self.menu.display_frame(screen)
        else:
            self.walls.draw(screen)
            draw_enviroment(screen)
            self.dots_group.draw(screen)
            self.enemies.draw(screen)
            screen.blit(self.player.image, self.player.rect)
            text = self.font.render("Score: " + str(self.score), True, ORANGE_RED)
            lives_text = self.font.render("Lives: " + str(self.lives), True, ORANGE_RED)
            if self.level == "easy":
                best_score = get_best_score(SCORE_FILE)
            else:
                best_score = get_best_score(SCORE_FILE_LVL2)
            best_score_text = self.font.render("Best score: " + str(best_score), True, ORANGE_RED)
            screen.blit(text, [50, 8])
            screen.blit(lives_text, [230, 8])
            screen.blit(best_score_text, [400, 8])

        pygame.display.flip()


class Menu(object):
    state = 0

    def __init__(self, items, font_color=BLACK, select_color=GREEN, ttf_font=ARCADE_FONT, font_size=15):
        self.font_color = font_color
        self.select_color = select_color
        self.items = items
        self.font = pygame.font.Font(ttf_font, font_size)
        self.title = pygame.image.load("images/tytul.jpg").convert_alpha()
        self.title = pygame.transform.scale(self.title, (TITLE_WIDTH, TITLE_HEIGHT))

        self.sound = pygame.mixer.Sound("sounds/are-you-sure-about-that.mp3")
        self.click = pygame.mixer.Sound("sounds/pacman_sound.ogg")

    def display_frame(self, screen):
        for index, item in enumerate(self.items):
            if self.state == index:
                if index == 5:
                    label = self.font.render(item, True, RED)
                else:
                    label = self.font.render(item, True, self.select_color)
            else:
                label = self.font.render(item, True, self.font_color)

            width = label.get_width()
            height = label.get_height()

            pos_x = (SCREEN_WIDTH / 2) - (width / 2)
            pos_y = (SCREEN_HEIGHT / 2) - (len(self.items) * height / 2) + (index * height * 1.5) + 50
            pos_title_x = (SCREEN_WIDTH / 2) - (TITLE_WIDTH / 2)
            pos_title_y = TITLE_HEIGHT / 2

            screen.blit(label, (pos_x, pos_y))
            screen.blit(self.title, (pos_title_x, pos_title_y))

    def event_handler(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                if self.state > 0:
                    self.state -= 1
                    self.click.play()

            elif event.key == pygame.K_DOWN:
                if self.state < len(self.items) - 1:
                    self.state += 1
                    self.click.play()
                if self.state == 5:
                    self.sound.play()
