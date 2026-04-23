import pygame
import math

class Paint:
    def __init__(self):
        self.WIDTH, self.HEIGHT = 800, 600
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        pygame.display.set_caption("Paint")
        self.font = pygame.font.SysFont(None, 24)
        self.clock = pygame.time.Clock()
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)
        self.BLUE = (0, 0, 255)
        self.screen.fill(self.WHITE)
        self.color = self.BLACK
        self.mode = "brush"
        self.drawing = False
        self.start_pos = None
        self.running = True

    def draw_ui(self):
        lines = [
            "1 - Brush   2 - Rect   3 - Circle   4 - Eraser",
            "R - Red   G - Green   B - Blue   K - Black"
        ]
        y = 10
        for line in lines:
            text = self.font.render(line, True, (0, 0, 0))
            self.screen.blit(text, (10, y))
            y += 25

    def run(self):
        while self.running:
            self.handle_events()
            self.draw_ui()
            pygame.display.flip()
            self.clock.tick(60)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.mode = "brush"
                elif event.key == pygame.K_2:
                    self.mode = "rect"
                elif event.key == pygame.K_3:
                    self.mode = "circle"
                elif event.key == pygame.K_4:
                    self.mode = "eraser"
                if event.key == pygame.K_r:
                    self.color = self.RED
                elif event.key == pygame.K_g:
                    self.color = self.GREEN
                elif event.key == pygame.K_b:
                    self.color = self.BLUE
                elif event.key == pygame.K_k:
                    self.color = self.BLACK

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.drawing = True
                self.start_pos = event.pos
            if event.type == pygame.MOUSEBUTTONUP:
                self.drawing = False
                end_pos = event.pos
                if self.mode == "rect":
                    rect = pygame.Rect(self.start_pos,
                        (end_pos[0] - self.start_pos[0],
                         end_pos[1] - self.start_pos[1]))
                    pygame.draw.rect(self.screen, self.color, rect, 2)
                elif self.mode == "circle":
                    radius = int(math.hypot(
                        end_pos[0] - self.start_pos[0],
                        end_pos[1] - self.start_pos[1]))
                    pygame.draw.circle(self.screen, self.color,
                                       self.start_pos, radius, 2)
            if event.type == pygame.MOUSEMOTION and self.drawing:
                if self.mode == "brush":
                    pygame.draw.circle(self.screen, self.color, event.pos, 5)
                elif self.mode == "eraser":
                    pygame.draw.circle(self.screen, self.WHITE, event.pos, 10)