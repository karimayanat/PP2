import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Enemy.png")
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = (random.randint(40, SCREEN_WIDTH-40), 0)

    def move(self):
        global SPEED
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (160, 520)

    def move(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0 and pressed_keys[pygame.K_LEFT]:
            self.rect.move_ip(-5, 0)

        if self.rect.right < SCREEN_WIDTH and pressed_keys[pygame.K_RIGHT]:
            self.rect.move_ip(5, 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.load_random_coin()
        self.rect = self.image.get_rect()
        self.reset()

    def load_random_coin(self):
        types = ["red", "green", "yellow"]
        self.type = random.choices(types, weights=[70, 20, 10])[0]

        if self.type == "red":
            img = pygame.image.load("images/coin_red.png")
            self.value = 1
        elif self.type == "green":
            img = pygame.image.load("images/coin_green.png")
            self.value = 3
        else:
            img = pygame.image.load("images/coin_yellow.png")
            self.value = 5

        self.image = pygame.transform.scale(img, (30, 30))

    def reset(self, enemy_rect=None):
        self.load_random_coin()
        while True:
            x = random.randint(40, SCREEN_WIDTH - 40)
            y = 0
            if enemy_rect is None or abs(x - enemy_rect.centerx) > 60:
                self.rect.center = (x, y)
                break

    def move(self):
        self.rect.move_ip(0, SPEED)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()