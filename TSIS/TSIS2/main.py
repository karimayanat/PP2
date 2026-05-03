import pygame
from paint import Paint

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Paint")
    clock = pygame.time.Clock()
    paint = Paint(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            paint.handle_event(event)
        paint.draw()
        pygame.display.flip()
        clock.tick(60)
    pygame.quit()
main()