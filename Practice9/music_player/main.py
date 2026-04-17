import pygame
import sys
from player import MusicPlayer

pygame.init()
screen = pygame.display.set_mode((500, 300))
pygame.display.set_caption("Music Player")
player = MusicPlayer()
font = pygame.font.SysFont(None, 30)

while True:
    screen.fill((255,255,255))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                player.play()
            elif event.key == pygame.K_s:
                player.stop()
            elif event.key == pygame.K_n:
                player.next()
            elif event.key == pygame.K_b:
                player.prev()
            elif event.key == pygame.K_q:
                pygame.quit()
                sys.exit()

    text = font.render("Track: " + player.current_track(), True, (0,0,0))
    screen.blit(text, (50, 100))
    pygame.display.flip()