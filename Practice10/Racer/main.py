import pygame
import sys
from racer import Player, Enemy, Coin, WIDTH, HEIGHT
pygame.init()
FPS = 60
WHITE = (255, 255, 255)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer")
clock = pygame.time.Clock()

font = pygame.font.SysFont("Verdana", 20)

player = Player()
enemy = Enemy()
coins = pygame.sprite.Group()

for i in range(3):
    coins.add(Coin())
score = 0

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    player.update()
    enemy.update()
    coins.update()

    if pygame.sprite.collide_rect(player, enemy):
        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        text_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        screen.fill((0, 0, 0))
        screen.blit(game_over_text, text_rect)
        pygame.display.update()
        pygame.time.delay(2500)
        pygame.quit()
        sys.exit()

    collected = pygame.sprite.spritecollide(player, coins, True)
    if collected:
        score += len(collected)
        for i in range(len(collected)):
            coins.add(Coin())

    screen.fill(WHITE)

    screen.blit(player.image, player.rect)
    screen.blit(enemy.image, enemy.rect)

    for coin in coins:
        screen.blit(coin.image, coin.rect)

    score_text = font.render(f"Coins: {score}", True, (0, 0, 0))
    screen.blit(score_text, (WIDTH - 120, 10))

    pygame.display.update()
    clock.tick(FPS)