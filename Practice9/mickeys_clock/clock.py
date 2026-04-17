import pygame
import math

def draw_clock(screen, minutes, seconds):
    center = (200, 200)
    min_angle = (minutes / 60) * 360
    sec_angle = (seconds / 60) * 360

    min_length = 100
    sec_length = 120

    min_x = center[0] + min_length * math.sin(math.radians(min_angle))
    min_y = center[1] - min_length * math.cos(math.radians(min_angle))

    sec_x = center[0] + sec_length * math.sin(math.radians(sec_angle))
    sec_y = center[1] - sec_length * math.cos(math.radians(sec_angle))

    pygame.draw.circle(screen, (0,0,0), center, 5)
    pygame.draw.line(screen, (0,0,255), center, (min_x, min_y), 5)
    pygame.draw.line(screen, (255,0,0), center, (sec_x, sec_y), 3)