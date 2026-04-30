import pygame, sys
from pygame.locals import *
import time
from racer import Player, Enemy, Coin, SPEED

pygame.init()

pygame.mixer.init()
pygame.mixer.music.load("sounds/background.wav")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

crash_sound = pygame.mixer.Sound("sounds/crash.wav")

FPS = 60
FramePerSec = pygame.time.Clock()
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCORE = 0
COINS = 0
RED = (255, 0, 0)
BLACK = (0, 0, 0)

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Game")

background = pygame.image.load("images/AnimatedStreet.png")

font = pygame.font.SysFont("Verdana", 60)
font_small = pygame.font.SysFont("Verdana", 20)
game_over = font.render("Game Over", True, BLACK)

P1 = Player()
E1 = Enemy()
C1 = Coin()

enemies = pygame.sprite.Group(E1)
coins = pygame.sprite.Group(C1)

all_sprites = pygame.sprite.Group(P1, E1, C1)

INC_SPEED = pygame.USEREVENT + 1
pygame.time.set_timer(INC_SPEED, 1000)
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        if event.type == INC_SPEED:
            import racer
            racer.SPEED += 0.2

    DISPLAYSURF.blit(background, (0,0))

    score_text = font_small.render(f"Score: {SCORE}", True, BLACK)
    coin_text = font_small.render(f"Coins: {COINS}", True, BLACK)
    DISPLAYSURF.blit(score_text, (10,10))
    DISPLAYSURF.blit(coin_text, (10,30))

    for entity in all_sprites:
        DISPLAYSURF.blit(entity.image, entity.rect)
        entity.move()

    if pygame.sprite.spritecollideany(P1, enemies):
        crash_sound.play()
        time.sleep(0.5)

        DISPLAYSURF.fill(RED)
        DISPLAYSURF.blit(game_over, (30,250))
        pygame.display.update()

        time.sleep(2)
        pygame.quit()
        sys.exit()

    collected = pygame.sprite.spritecollide(P1, coins, False)

    for coin in collected:
        COINS += coin.value
        coin.reset()
        if COINS % 10 == 0:
            import racer
            racer.SPEED += 1

    pygame.display.update()
    FramePerSec.tick(FPS)