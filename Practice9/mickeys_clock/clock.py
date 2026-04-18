import pygame
import datetime

class MickeyClock:
    def __init__(self):
        self.bg = pygame.image.load('images/mainclock.png')
        self.bg = pygame.transform.scale(self.bg, (600, 600))
        self.min_arm = pygame.image.load('images/rightarm.png')
        self.min_arm = pygame.transform.scale(self.min_arm, (800, 700))
        self.sec_arm = pygame.image.load('images/leftarm.png')
        self.sec_arm = pygame.transform.scale(self.sec_arm, (40, 500))

    def get_angles(self):
        now = datetime.datetime.now()
        angle_min = now.minute * -6
        angle_sec = now.second * -6
        return angle_min, angle_sec

    def draw(self, screen):
        angle_min, angle_sec = self.get_angles()
        center = (screen.get_width() // 2, screen.get_height() // 2)
        rotated_min = pygame.transform.rotate(self.min_arm, angle_min)
        rotated_sec = pygame.transform.rotate(self.sec_arm, angle_sec)
        bg_rect = self.bg.get_rect(center=center)
        screen.blit(self.bg, bg_rect)
        sec_rect = rotated_sec.get_rect(center=center)
        screen.blit(rotated_sec, sec_rect)
        min_rect = rotated_min.get_rect(center=center)
        screen.blit(rotated_min, min_rect)