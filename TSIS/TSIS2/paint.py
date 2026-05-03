import pygame
import math
from datetime import datetime

from tools import (
    draw_line, draw_rect, draw_circle,
    draw_polygon, flood_fill
)

class Paint:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("Arial", 18)
        self.color = (0, 0, 255)
        self.mode = 'pencil'
        self.brush_size = 5
        self.drawing = False
        self.start_pos = None
        self.last_pos = None
        self.canvas = pygame.Surface(self.screen.get_size())
        self.canvas.fill((255, 255, 255))
        self.preview = pygame.Surface(self.screen.get_size(), pygame.SRCALPHA)
        self.text_mode = False
        self.text_pos = None
        self.text_input = ""

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_CTRL:
                filename = datetime.now().strftime("drawing_%Y%m%d_%H%M%S.png")
                pygame.image.save(self.canvas, filename)
                print("Saved:", filename)

            elif event.key == pygame.K_r:
                self.color = (255, 0, 0)
            elif event.key == pygame.K_g:
                self.color = (0, 255, 0)
            elif event.key == pygame.K_b:
                self.color = (0, 0, 255)

            elif event.key == pygame.K_1:
                self.brush_size = 2
            elif event.key == pygame.K_2:
                self.brush_size = 5
            elif event.key == pygame.K_3:
                self.brush_size = 10

            elif event.key == pygame.K_p:
                self.mode = 'pencil'
            elif event.key == pygame.K_l:
                self.mode = 'line'
            elif event.key == pygame.K_f:
                self.mode = 'fill'
            elif event.key == pygame.K_t:
                self.mode = 'text'
            elif event.key == pygame.K_e:
                self.mode = 'eraser'
            elif event.key == pygame.K_4:
                self.mode = 'rect'
            elif event.key == pygame.K_5:
                self.mode = 'circle'
            elif event.key == pygame.K_6:
                self.mode = 'square'
            elif event.key == pygame.K_7:
                self.mode = 'right_triangle'
            elif event.key == pygame.K_8:
                self.mode = 'equilateral_triangle'
            elif event.key == pygame.K_9:
                self.mode = 'rhombus'

            if self.text_mode:
                if event.key == pygame.K_RETURN:
                    img = self.font.render(self.text_input, True, self.color)
                    self.canvas.blit(img, self.text_pos)
                    self.text_mode = False
                    self.text_input = ""

                elif event.key == pygame.K_ESCAPE:
                    self.text_mode = False
                    self.text_input = ""

                elif event.key == pygame.K_BACKSPACE:
                    self.text_input = self.text_input[:-1]

                else:
                    self.text_input += event.unicode

        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.start_pos = event.pos
            self.last_pos = event.pos
            self.drawing = True
            if self.mode == 'fill':
                flood_fill(self.canvas, event.pos, self.color)
            elif self.mode == 'text':
                self.text_mode = True
                self.text_pos = event.pos
                self.text_input = ""

        elif event.type == pygame.MOUSEBUTTONUP:
            self.drawing = False
            end_pos = event.pos
            if self.mode == 'line':
                draw_line(self.canvas, self.color,
                          self.start_pos, end_pos, self.brush_size)

            elif self.mode == 'rect':
                draw_rect(self.canvas, self.color,
                          self.start_pos, end_pos, self.brush_size)

            elif self.mode == 'circle':
                r = int(math.hypot(end_pos[0]-self.start_pos[0],
                                   end_pos[1]-self.start_pos[1]))
                draw_circle(self.canvas, self.color,
                            self.start_pos, r, self.brush_size)

            elif self.mode == 'square':
                side = max(abs(end_pos[0]-self.start_pos[0]),
                           abs(end_pos[1]-self.start_pos[1]))
                rect = (self.start_pos[0], self.start_pos[1],
                        side, side)
                pygame.draw.rect(self.canvas, self.color, rect, self.brush_size)

            elif self.mode == 'right_triangle':
                points = [self.start_pos,
                          (self.start_pos[0], end_pos[1]),
                          end_pos]
                draw_polygon(self.canvas, self.color, points, self.brush_size)

            elif self.mode == 'equilateral_triangle':
                side = abs(end_pos[0] - self.start_pos[0])
                height = int(side * math.sqrt(3) / 2)
                p1 = self.start_pos
                p2 = (self.start_pos[0] + side, self.start_pos[1])
                p3 = (self.start_pos[0] + side // 2,
                      self.start_pos[1] - height)
                draw_polygon(self.canvas, self.color,
                             [p1, p2, p3], self.brush_size)
            
            elif self.mode == 'rhombus':
                cx = (self.start_pos[0] + end_pos[0]) // 2
                cy = (self.start_pos[1] + end_pos[1]) // 2
                points = [
                    (cx, self.start_pos[1]),
                    (end_pos[0], cy),
                    (cx, end_pos[1]),
                    (self.start_pos[0], cy)
                ]
                draw_polygon(self.canvas, self.color,
                             points, self.brush_size)
            self.preview.fill((0, 0, 0, 0))

        elif event.type == pygame.MOUSEMOTION and self.drawing:
            current = event.pos
            if self.mode == 'pencil':
                draw_line(self.canvas, self.color,
                          self.last_pos, current, self.brush_size)
            elif self.mode == 'eraser':
                draw_line(self.canvas, (255, 255, 255),
                          self.last_pos, current, self.brush_size)
            elif self.mode == 'line':
                self.preview.fill((0, 0, 0, 0))
                pygame.draw.line(self.preview, self.color,
                                 self.start_pos, current, self.brush_size)
            self.last_pos = current

    def draw_ui(self):
        y = 10
        info = [
            "P pencil | L line | F fill | T text | E eraser",
            "1/2/3 brush size",
            "R/G/B colors",
            "4-9 shapes",
            "CTRL+S save"
        ]
        for i in info:
            self.screen.blit(self.font.render(i, True, (0, 0, 0)), (10, y))
            y += 20
        mode = f"Mode: {self.mode} | Size: {self.brush_size}"
        self.screen.blit(self.font.render(mode, True, (0, 0, 0)), (10, y + 10))
        if self.text_mode:
            txt = self.font.render(self.text_input, True, self.color)
            self.screen.blit(txt, self.text_pos)

    def draw(self):
        self.screen.blit(self.canvas, (0, 0))
        self.screen.blit(self.preview, (0, 0))
        self.draw_ui()