import pygame
import math

class Paint:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 18)

        self.color = (0, 0, 255)
        self.mode = 'line'

        self.drawing = False
        self.start_pos = None
        self.canvas = pygame.Surface(self.screen.get_size())
        self.canvas.fill((255, 255, 255))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                self.color = (255, 0, 0)
            elif event.key == pygame.K_g:
                self.color = (0, 255, 0)
            elif event.key == pygame.K_b:
                self.color = (0, 0, 255)

            elif event.key == pygame.K_1:
                self.mode = 'line'
            elif event.key == pygame.K_2:
                self.mode = 'rect'
            elif event.key == pygame.K_3:
                self.mode = 'circle'
            elif event.key == pygame.K_4:
                self.mode = 'square'
            elif event.key == pygame.K_5:
                self.mode = 'right_triangle'
            elif event.key == pygame.K_6:
                self.mode = 'equilateral_triangle'
            elif event.key == pygame.K_7:
                self.mode = 'rhombus'
            elif event.key == pygame.K_e:
                self.mode = 'eraser'

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.drawing = True
            self.start_pos = event.pos
            self.last_pos = event.pos

        elif event.type == pygame.MOUSEBUTTONUP:
            self.drawing = False
            end_pos = event.pos
            self.last_pos = None

            if self.mode == 'rect':
                rect = pygame.Rect(self.start_pos,
                                (end_pos[0]-self.start_pos[0],
                                    end_pos[1]-self.start_pos[1]))
                pygame.draw.rect(self.canvas, self.color, rect, 2)

            elif self.mode == 'circle':
                r = int(math.hypot(end_pos[0]-self.start_pos[0],
                                end_pos[1]-self.start_pos[1]))
                pygame.draw.circle(self.canvas, self.color, self.start_pos, r, 2)

            elif self.mode == 'square':
                side = max(abs(end_pos[0]-self.start_pos[0]),
                        abs(end_pos[1]-self.start_pos[1]))
                rect = pygame.Rect(self.start_pos, (side, side))
                pygame.draw.rect(self.canvas, self.color, rect, 2)

            elif self.mode == 'right_triangle':
                points = [self.start_pos,
                        (self.start_pos[0], end_pos[1]),
                        end_pos]
                pygame.draw.polygon(self.canvas, self.color, points, 2)

            elif self.mode == 'equilateral_triangle':
                side = abs(end_pos[0] - self.start_pos[0])
                height = int(side * math.sqrt(3) / 2)

                p1 = self.start_pos
                p2 = (self.start_pos[0] + side, self.start_pos[1])
                p3 = (self.start_pos[0] + side // 2,
                    self.start_pos[1] - height)

                pygame.draw.polygon(self.canvas, self.color, [p1, p2, p3], 2)

            elif self.mode == 'rhombus':
                cx = (self.start_pos[0] + end_pos[0]) // 2
                cy = (self.start_pos[1] + end_pos[1]) // 2

                points = [
                    (cx, self.start_pos[1]),
                    (end_pos[0], cy),
                    (cx, end_pos[1]),
                    (self.start_pos[0], cy)
                ]
                pygame.draw.polygon(self.canvas, self.color, points, 2)

        elif event.type == pygame.MOUSEMOTION:
            if self.drawing:
                current_pos = event.pos
                if self.drawing and self.mode == 'line':
                    pygame.draw.line(self.canvas, self.color, self.last_pos, current_pos, 5)

                elif self.mode == 'eraser':
                    pygame.draw.line(self.canvas, (255, 255, 255), self.last_pos, current_pos, 30)

                self.last_pos = current_pos

    def draw_ui(self):
        instructions = [
            "R/G/B - color",
            "1-line  2-rect  3-circle",
            "4-square 5-right triangle",
            "6-equilateral 7-rhombus",
            "E - eraser"
        ]

        y = 10
        for text in instructions:
            img = self.font.render(text, True, (0, 0, 0))
            self.screen.blit(img, (10, y))
            y += 20

        mode_text = self.font.render(f"Mode: {self.mode}", True, (0, 0, 0))
        self.screen.blit(mode_text, (10, y + 10))

    def draw(self):
        self.screen.blit(self.canvas, (0, 0))
        self.draw_ui()