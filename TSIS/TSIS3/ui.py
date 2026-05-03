import pygame
import sys
from persistence import load_scores, load_settings, save_settings

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (200, 0, 0)
GRAY = (100, 100, 100)

def draw_text(surf, text, size, x, y, color=BLACK):
    font = pygame.font.SysFont("Verdana", size)
    txt = font.render(text, True, color)
    surf.blit(txt, txt.get_rect(center=(x, y)))

def get_username(screen):
    name = ""
    while True:
        screen.fill(WHITE)
        draw_text(screen, "Enter Username:", 30, 200, 250)
        draw_text(screen, name + "_", 30, 200, 300, RED)
        draw_text(screen, "Press ENTER to Start", 20, 200, 400, GRAY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and name != "": return name
                elif event.key == pygame.K_BACKSPACE: name = name[:-1]
                else: 
                    if len(name) < 10: name += event.unicode

def draw_menu(screen):
    while True:
        screen.fill(WHITE)
        draw_text(screen, "RACER PRO", 50, 200, 150)
        buttons = ["Play", "Leaderboard", "Settings", "Quit"]
        for i, b in enumerate(buttons):
            draw_text(screen, f"{i+1}. {b}", 30, 200, 250 + i*50)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: return "play"
                if event.key == pygame.K_2: return "leaderboard"
                if event.key == pygame.K_3: return "settings"
                if event.key == pygame.K_4: sys.exit()

def draw_settings(screen):
    settings = load_settings()
    while True:
        screen.fill(WHITE)
        draw_text(screen, "SETTINGS", 40, 200, 100)
        draw_text(screen, f"1. Volume: {settings['volume']}", 25, 200, 200)
        draw_text(screen, f"2. Car: {settings['car_color']}", 25, 200, 250)
        draw_text(screen, f"3. Diff: {settings['difficulty']}", 25, 200, 300)
        draw_text(screen, "Press ESC to Save & Back", 20, 200, 450, GRAY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: settings['volume'] = round((settings['volume'] + 0.1) % 1.1, 1)
                if event.key == pygame.K_2: settings['car_color'] = "blue" if settings['car_color'] == "red" else "red"
                if event.key == pygame.K_3: 
                    diffs = ["Easy", "Medium", "Hard"]
                    settings['difficulty'] = diffs[(diffs.index(settings['difficulty'])+1)%3]
                if event.key == pygame.K_ESCAPE:
                    save_settings(settings)
                    return settings

def draw_leaderboard(screen):
    scores = load_scores()
    while True:
        screen.fill(WHITE)
        draw_text(screen, "TOP 10 RACERS", 35, 200, 50)
        for i, s in enumerate(scores):
            txt = f"{i+1}. {s['name']} - {s['score']} pts"
            draw_text(screen, txt, 20, 200, 110 + i*35)
        draw_text(screen, "Press ESC to Menu", 20, 200, 550, GRAY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return

def draw_game_over(screen, score, coins, distance):
    while True:
        screen.fill(BLACK)
        draw_text(screen, "CRASHED!", 50, 200, 150, RED)
        draw_text(screen, f"Score: {score}", 30, 200, 250, WHITE)
        draw_text(screen, f"Distance: {distance}m", 25, 200, 300, WHITE)
        draw_text(screen, "R - Retry | M - Menu", 20, 200, 450, GRAY)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r: return "retry"
                if event.key == pygame.K_m: return "menu"