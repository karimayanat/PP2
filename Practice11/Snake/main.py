import pygame
import sys
from snake import Game

pygame.init()

CELL_SIZE = 20
GRID_SIZE = 30
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake")

font = pygame.font.SysFont("Arial", 24)

game = Game()
game_over = False

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if event.type == pygame.KEYDOWN:
            if not game_over:
                if event.key == pygame.K_UP:
                    game.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    game.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    game.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.change_direction("RIGHT")

            if game_over and event.key == pygame.K_r:
                game = Game()
                game_over = False

    if not game_over:
        alive = game.move()
        if not alive:
            game_over = True

    game.draw(screen, font)

    if game_over:
        text1 = font.render("GAME OVER", True, (255, 255, 255))
        text2 = font.render(f"Score: {game.score}", True, (255, 255, 255))
        text3 = font.render("Press R to restart", True, (255, 255, 255))

        screen.blit(text1, (WIDTH//2 - 90, HEIGHT//2 - 40))
        screen.blit(text2, (WIDTH//2 - 70, HEIGHT//2))
        screen.blit(text3, (WIDTH//2 - 130, HEIGHT//2 + 40))

    pygame.display.flip()
    game.clock.tick(game.speed)