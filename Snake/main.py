import pygame
import sys
from pygame.math import Vector2
import random


class Snake:
    def __init__(self):
        self.body = [Vector2(10, 9), Vector2(10, 10), Vector2(10, 11)]
        self.direction = Vector2(0, -1)
        self.new_block = False
        self.direction_queue = []

        self.head_up = pygame.image.load('Graphics/head_up.png').convert_alpha()
        self.head_down = pygame.image.load('Graphics/head_down.png').convert_alpha()
        self.head_right = pygame.image.load('Graphics/head_right.png').convert_alpha()
        self.head_left = pygame.image.load('Graphics/head_left.png').convert_alpha()

        self.tail_up = pygame.image.load('Graphics/tail_up.png').convert_alpha()
        self.tail_down = pygame.image.load('Graphics/tail_down.png').convert_alpha()
        self.tail_right = pygame.image.load('Graphics/tail_right.png').convert_alpha()
        self.tail_left = pygame.image.load('Graphics/tail_left.png').convert_alpha()

        self.body_vertical = pygame.image.load('Graphics/body_vertical.png').convert_alpha()
        self.body_horizontal = pygame.image.load('Graphics/body_horizontal.png').convert_alpha()

        self.body_tr = pygame.image.load('Graphics/body_tr.png').convert_alpha()
        self.body_tl = pygame.image.load('Graphics/body_tl.png').convert_alpha()
        self.body_br = pygame.image.load('Graphics/body_br.png').convert_alpha()
        self.body_bl = pygame.image.load('Graphics/body_bl.png').convert_alpha()

        self.crunch_sound = pygame.mixer.Sound('Sound/crunch.wav')
        self.crunch_sound.set_volume(0.02)

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()
        for index, block in enumerate(self.body):
            snake_rect = pygame.Rect(int(block.x * cell_size), int(block.y * cell_size), cell_size, cell_size)
            if index == 0:
                screen.blit(self.head, snake_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, snake_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block
                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, snake_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, snake_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, snake_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, snake_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, snake_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, snake_rect)

    def move_snake(self):
        if self.direction_queue:
            self.direction = self.direction_queue.pop(0)
        if self.new_block:
            body_copy = self.body[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
        body_copy.insert(0, body_copy[0] + self.direction)
        self.body = body_copy

    def add_block(self):
        self.new_block = True

    def update_head_graphics(self):
        if self.direction.y == -1:
            self.head = self.head_up
        elif self.direction.y == 1:
            self.head = self.head_down
        elif self.direction.x == -1:
            self.head = self.head_left
        else:
            self.head = self.head_right

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down
        else:
            self.tail = self.tail_up


class Fruit:
    def __init__(self):
        self.randomise()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(apple, fruit_rect)

    def randomise(self):
        self.pos = Vector2(random.randint(0, cell_number - 1), random.randint(0, cell_number - 1))


class Main:
    def __init__(self):
        self.snake = Snake()
        self.fruit = Fruit()
        self.game_over = False
        self.background_music = pygame.mixer.Sound('Sound/Wii Music - Gaming Background Music (HD).mp3')
        self.background_music.set_volume(0.03)
        self.background_music.play(-1)

    def update(self):
        if not self.game_over:
            self.snake.move_snake()
            self.check_collision()
            self.check_game_over()

    def draw_elements(self):
        if self.game_over:
            self.show_game_over()
        else:
            self.draw_grass()
            self.draw_score()
            self.snake.draw_snake()
            self.fruit.draw_fruit()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomise()
            self.snake.add_block()
            self.snake.crunch_sound.play()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomise()

    def check_game_over(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over = True
        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over = True

    def reset(self):
        self.snake.direction = Vector2(0, -1)
        self.snake.direction_queue = []
        self.snake.body = [Vector2(10, 9), Vector2(10, 10), Vector2(10, 11)]
        self.snake.new_block = False
        self.game_over = False

    @staticmethod
    def draw_grass():
        grass_color = (167, 209, 61)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 == 1:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = 'Score: ' + str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (54, 70, 15))
        score_text_x_pos = int(cell_size * cell_number - 40)
        score_text_y_pos = int(cell_size)
        score_rect = score_surface.get_rect(center=(score_text_x_pos, score_text_y_pos))
        background_rect = pygame.Rect(score_rect.left - 2, score_rect.top, score_rect.width + 6, score_rect.height)
        pygame.draw.rect(screen, (167, 210, 63), background_rect)
        screen.blit(score_surface, score_rect)
        pygame.draw.rect(screen, (54, 70, 15), background_rect, 2)

    def show_game_over(self):
        game_over_surface = game_font.render('Game Over', True, (255, 0, 0))
        game_over_rect = game_over_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2))
        screen.blit(game_over_surface, game_over_rect)
        restart_surface = game_font.render('Press R to Restart', True, (0, 0, 0))
        restart_rect = restart_surface.get_rect(center=(cell_size * cell_number // 2, cell_size * cell_number // 2 + 40))
        screen.blit(restart_surface, restart_rect)


pygame.mixer.pre_init(44100, -16, 2, 512)
pygame.init()
pygame.display.set_caption('Snake')
cell_size = 33
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
apple = pygame.image.load('Graphics/apple1.png').convert_alpha()
game_font = pygame.font.Font('Font/Spring Nature.otf', 22)

game = Main()

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 125)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == SCREEN_UPDATE:
            game.update()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w or event.key == pygame.K_UP:
                if not game.snake.direction == Vector2(0, 1):
                    game.snake.direction_queue.append(Vector2(0, -1))
            if event.key == pygame.K_s or event.key == pygame.K_DOWN:
                if not game.snake.direction == Vector2(0, -1):
                    game.snake.direction_queue.append(Vector2(0, 1))
            if event.key == pygame.K_a or event.key == pygame.K_LEFT:
                if not game.snake.direction == Vector2(1, 0):
                    game.snake.direction_queue.append(Vector2(-1, 0))
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                if not game.snake.direction == Vector2(-1, 0):
                    game.snake.direction_queue.append(Vector2(1, 0))
            if event.key == pygame.K_r and game.game_over:
                game.reset()

    screen.fill((175, 215, 70))
    game.draw_elements()
    pygame.display.update()
    clock.tick(60)
