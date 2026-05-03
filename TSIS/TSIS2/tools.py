import pygame
from collections import deque

def draw_line(surface, color, start, end, size):
    pygame.draw.line(surface, color, start, end, size)

def draw_rect(surface, color, start, end, size):
    rect = pygame.Rect(start, (end[0] - start[0], end[1] - start[1]))
    pygame.draw.rect(surface, color, rect, size)

def draw_circle(surface, color, center, radius, size):
    pygame.draw.circle(surface, color, center, radius, size)

def draw_polygon(surface, color, points, size):
    pygame.draw.polygon(surface, color, points, size)

def flood_fill(surface, pos, new_color):
    target_color = surface.get_at(pos)
    if target_color == new_color:
        return
    q = deque([pos])
    w, h = surface.get_size()
    while q:
        x, y = q.popleft()
        if x < 0 or y < 0 or x >= w or y >= h:
            continue
        if surface.get_at((x, y)) != target_color:
            continue
        surface.set_at((x, y), new_color)
        q.extend([
            (x + 1, y), (x - 1, y),
            (x, y + 1), (x, y - 1)
        ])