import pygame
import sys
from ball import Ball
pygame.init()
WIDTH, HEIGHT = 600, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Moving Ball")
ball = Ball(300, 200)
clock = pygame.time.Clock()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT]:
        ball.move(-10, 0)
    if keys[pygame.K_RIGHT]:
        ball.move(10, 0)
    if keys[pygame.K_UP]:
        ball.move(0, -10)
    if keys[pygame.K_DOWN]:
        ball.move(0, 10)
    screen.fill((255,255,255))
    ball.draw(screen)
    pygame.display.flip()
    clock.tick(60)