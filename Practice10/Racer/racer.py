import pygame
import random

WIDTH = 400
HEIGHT = 600

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/player.png")
        self.image = pygame.transform.scale(self.image, (80, 100))
        self.rect = self.image.get_rect(
            midbottom=(WIDTH // 2, HEIGHT - 10)
        )
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= 5
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += 5

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/enemy.png")
        self.image = pygame.transform.scale(self.image, (50, 100))
        self.rect = self.image.get_rect(
            midtop=(random.randint(40, WIDTH - 40), -120)
        )
    def update(self):
        self.rect.y += 5
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(40, WIDTH - 40), 0)

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("images/coin.png")
        self.image = pygame.transform.scale(self.image, (40, 40))
        self.rect = self.image.get_rect(
            center=(random.randint(40, WIDTH - 40),
                    random.randint(-100, -40))
        )
    def update(self):
        self.rect.y += 4
        if self.rect.top > HEIGHT:
            self.rect.center = (
                random.randint(40, WIDTH - 40),
                random.randint(-100, -40)
            )