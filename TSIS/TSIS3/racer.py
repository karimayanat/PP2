import pygame
import random

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SPEED = 5
LANES = [60, 150, 250, 340]

active_objects = pygame.sprite.Group()

def spawn_free_position():
    attempts = 0
    while attempts < 50:
        x = random.choice(LANES)
        y = random.randint(-600, -50)
        new_rect = pygame.Rect(x-20, y-20, 40, 40)
        
        overlap = any(new_rect.colliderect(obj.rect.inflate(30, 30)) for obj in active_objects)
        if not overlap:
            return (x, y)
        attempts += 1
    return (random.choice(LANES), -100)

class Player(pygame.sprite.Sprite):
    def __init__(self, color="red"):
        super().__init__()
        try:
            self.image = pygame.image.load(f"assets/images/Player_{color}.png")
        except:
            self.image = pygame.image.load("assets/images/Player.png")
        self.rect = self.image.get_rect()
        self.rect.center = (200, 520)

    def move(self):
        keys = pygame.key.get_pressed()
        if self.rect.left > 0 and keys[pygame.K_LEFT]:
            self.rect.move_ip(-7, 0)
        if self.rect.right < SCREEN_WIDTH and keys[pygame.K_RIGHT]:
            self.rect.move_ip(7, 0)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/images/Enemy.png")
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = spawn_free_position()

    def move(self, current_speed):
        self.rect.move_ip(0, current_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class Hazard(pygame.sprite.Sprite):
    def __init__(self, h_type="oil"):
        super().__init__()
        self.type = h_type
        img = pygame.image.load(f"assets/images/{h_type}.png")
        self.image = pygame.transform.scale(img, (40, 40))
        self.rect = self.image.get_rect()
        self.reset()

    def reset(self):
        self.rect.center = spawn_free_position()

    def move(self, current_speed):
        self.rect.move_ip(0, current_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,0,30,30)
        self.reset()

    def reset(self):
        types = ["red", "green", "yellow"]
        self.val_type = random.choices(types, weights=[70, 20, 10])[0]
        self.value = {"red": 1, "green": 5, "yellow": 10}[self.val_type]
        img = pygame.image.load(f"assets/images/coin_{self.val_type}.png")
        self.image = pygame.transform.scale(img, (30, 30))
        self.rect = self.image.get_rect(center=spawn_free_position())

    def move(self, current_speed):
        self.rect.move_ip(0, current_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.reset()

class PowerUp(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.rect = pygame.Rect(0,0,35,35)
        self.reset()

    def reset(self):
        self.p_type = random.choice(["nitro", "shield", "repair"])
        img = pygame.image.load(f"assets/images/{self.p_type}.png")
        self.image = pygame.transform.scale(img, (35, 35))
        self.rect = self.image.get_rect(center=spawn_free_position())
        self.spawn_time = pygame.time.get_ticks()

    def move(self, current_speed):
        self.rect.move_ip(0, current_speed)
        if self.rect.top > SCREEN_HEIGHT or pygame.time.get_ticks() - self.spawn_time > 8000:
            self.reset()

def register(obj):
    if obj not in active_objects:
        active_objects.add(obj)

def unregister(obj):
    if obj in active_objects:
        active_objects.remove(obj)