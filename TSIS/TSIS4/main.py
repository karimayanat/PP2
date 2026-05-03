import pygame
import sys
import json
import os
from game import Game
from db import Database

pygame.init()

CELL_SIZE = 20
GRID_SIZE = 30
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 0, 255)
GREEN = (0, 200, 0)
RED = (255, 0, 0)

class Settings:
    def __init__(self):
        self.load_settings()
    
    def load_settings(self):
        if os.path.exists("settings.json"):
            with open("settings.json", "r") as f:
                data = json.load(f)
                self.snake_color = tuple(data.get("snake_color", [0, 200, 0]))
                self.grid_overlay = data.get("grid_overlay", True)
        else:
            self.snake_color = (0, 200, 0)
            self.grid_overlay = True
    
    def save_settings(self):
        with open("settings.json", "w") as f:
            json.dump({
                "snake_color": list(self.snake_color),
                "grid_overlay": self.grid_overlay
            }, f)

class Button:
    def __init__(self, x, y, width, height, text, color, hover_color):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.current_color = color
        self.font = pygame.font.Font(None, 32)
    
    def draw(self, screen):
        pygame.draw.rect(screen, self.current_color, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = self.font.render(self.text, True, WHITE)
        text_rect = text_surface.get_rect(center=self.rect.center)
        screen.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            if self.rect.collidepoint(event.pos):
                self.current_color = self.hover_color
            else:
                self.current_color = self.color
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False

class UsernameInput:
    def __init__(self):
        self.username = ""
        self.active = True
        self.font = pygame.font.Font(None, 36)
        self.rect = pygame.Rect(WIDTH//2 - 120, HEIGHT//2 - 20, 240, 40)
    
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN and self.username:
                return False
            elif event.key == pygame.K_BACKSPACE:
                self.username = self.username[:-1]
            elif len(self.username) < 20 and event.unicode.isalnum():
                self.username += event.unicode
        return True
    
    def draw(self, screen):
        pygame.draw.rect(screen, DARK_GRAY, self.rect)
        pygame.draw.rect(screen, WHITE, self.rect, 2)
        text_surface = self.font.render(self.username + ("_" if self.active else ""), True, WHITE)
        screen.blit(text_surface, (self.rect.x + 10, self.rect.y + 8))
        label_font = pygame.font.Font(None, 28)
        label = label_font.render("Enter username:", True, WHITE)
        screen.blit(label, (WIDTH//2 - 80, HEIGHT//2 - 50))

def main_menu(settings, db):
    buttons = [
        Button(WIDTH//2 - 80, HEIGHT//2 - 80, 160, 45, "Play", GREEN, (0, 150, 0)),
        Button(WIDTH//2 - 80, HEIGHT//2 - 20, 160, 45, "Leaderboard", BLUE, (0, 0, 150)),
        Button(WIDTH//2 - 80, HEIGHT//2 + 40, 160, 45, "Settings", GRAY, (50, 50, 50)),
        Button(WIDTH//2 - 80, HEIGHT//2 + 100, 160, 45, "Quit", RED, (150, 0, 0))
    ]
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit", None
            
            for button in buttons:
                if button.handle_event(event):
                    if button.text == "Play":
                        username_input = UsernameInput()
                        while True:
                            for e in pygame.event.get():
                                if e.type == pygame.QUIT:
                                    return "quit", None
                                if username_input.handle_event(e) == False:
                                    if username_input.username:
                                        return "play", username_input.username
                            
                            screen.fill(BLACK)
                            username_input.draw(screen)
                            pygame.display.flip()
                            clock.tick(30)
                    
                    elif button.text == "Leaderboard":
                        return "leaderboard", None
                    
                    elif button.text == "Settings":
                        new_settings = settings_screen(settings)
                        if new_settings is not None:
                            return "settings", new_settings
                        else:
                            return "quit", None
                    
                    elif button.text == "Quit":
                        return "quit", None
        
        screen.fill(BLACK)
        title_font = pygame.font.Font(None, 56)
        title = title_font.render("SNAKE GAME", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, HEIGHT//2 - 180))
        
        for button in buttons:
            button.draw(screen)
        
        pygame.display.flip()
        clock.tick(60)

def leaderboard_screen(db):
    font_small = pygame.font.Font(None, 18)
    font_medium = pygame.font.Font(None, 28)
    back_button = Button(WIDTH//2 - 50, HEIGHT - 50, 100, 35, "Back", GRAY, DARK_GRAY)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            if back_button.handle_event(event):
                return "menu"
        
        screen.fill(BLACK)
        
        title = font_medium.render("TOP 10 SCORES", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 15))
        
        headers = ["#", "Username", "Score", "Lvl", "Date"]
        x_positions = [20, 80, 200, 280, 350]
        for i, header in enumerate(headers):
            header_text = font_small.render(header, True, WHITE)
            screen.blit(header_text, (x_positions[i], 55))
        
        top_scores = db.get_top_scores()
        
        y = 80
        for i, score_data in enumerate(top_scores, 1):
            if y > HEIGHT - 70:
                break
                
            rank_text = font_small.render(str(i), True, WHITE)
            username_text = font_small.render(score_data[0][:15], True, WHITE)
            score_text = font_small.render(str(score_data[1]), True, WHITE)
            level_text = font_small.render(str(score_data[2]), True, WHITE)
            
            try:
                if hasattr(score_data[3], 'strftime'):
                    date_str = score_data[3].strftime("%m/%d")
                else:
                    date_str = str(score_data[3])[:5]
            except:
                date_str = "N/A"
            
            date_text = font_small.render(date_str, True, WHITE)
            
            screen.blit(rank_text, (x_positions[0], y))
            screen.blit(username_text, (x_positions[1], y))
            screen.blit(score_text, (x_positions[2], y))
            screen.blit(level_text, (x_positions[3], y))
            screen.blit(date_text, (x_positions[4], y))
            y += 22
        
        back_button.draw(screen)
        pygame.display.flip()
        clock.tick(60)

def settings_screen(settings):
    temp_settings = Settings()
    temp_settings.snake_color = settings.snake_color
    temp_settings.grid_overlay = settings.grid_overlay
    
    back_button = Button(WIDTH//2 - 50, HEIGHT - 50, 100, 35, "Save & Back", GRAY, DARK_GRAY)
    
    color_buttons = []
    colors = [(0, 200, 0), (0, 0, 255), (255, 165, 0), (200, 0, 200)]
    color_names = ["Green", "Blue", "Orange", "Purple"]
    start_x = WIDTH//2 - 170
    for i, color in enumerate(colors):
        btn = Button(start_x + i * 85, HEIGHT//2 - 20, 70, 70, "", color, color)
        btn.text = ""
        color_buttons.append((btn, color))
    
    grid_toggle = Button(WIDTH//2 - 80, HEIGHT//2 + 70, 160, 35, 
                         f"Grid: {'ON' if temp_settings.grid_overlay else 'OFF'}", 
                         GRAY, DARK_GRAY)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None
            
            if back_button.handle_event(event):
                settings.snake_color = temp_settings.snake_color
                settings.grid_overlay = temp_settings.grid_overlay
                settings.save_settings()
                return settings
            
            if grid_toggle.handle_event(event):
                temp_settings.grid_overlay = not temp_settings.grid_overlay
                grid_toggle.text = f"Grid: {'ON' if temp_settings.grid_overlay else 'OFF'}"
            
            for btn, color in color_buttons:
                if btn.handle_event(event):
                    temp_settings.snake_color = color
        
        screen.fill(BLACK)
        
        font = pygame.font.Font(None, 40)
        title = font.render("SETTINGS", True, GREEN)
        screen.blit(title, (WIDTH//2 - title.get_width()//2, 30))
        
        label_font = pygame.font.Font(None, 24)
        color_label = label_font.render("Snake Color:", True, WHITE)
        screen.blit(color_label, (WIDTH//2 - 60, HEIGHT//2 - 70))
        
        for btn, color in color_buttons:
            btn.draw(screen)
            if color == temp_settings.snake_color:
                pygame.draw.rect(screen, WHITE, btn.rect, 3)
        
        grid_toggle.draw(screen)
        back_button.draw(screen)
        
        info_font = pygame.font.Font(None, 16)
        info = info_font.render("Click on colors to change", True, GRAY)
        screen.blit(info, (WIDTH//2 - 90, HEIGHT - 25))
        
        pygame.display.flip()
        clock.tick(60)

def game_loop(username, settings, db):
    game = Game(username, settings, db)
    game_over = False
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "quit"
            
            if event.type == pygame.KEYDOWN and not game_over:
                if event.key == pygame.K_UP:
                    game.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    game.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    game.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.change_direction("RIGHT")
        
        if not game_over:
            game_over = not game.update()
        
        game.draw(screen)
        
        if game_over:
            font_big = pygame.font.Font(None, 40)
            font_small = pygame.font.Font(None, 24)
            
            retry_btn = Button(WIDTH//2 - 80, HEIGHT//2 + 40, 150, 40, "Retry", GREEN, (0, 150, 0))
            menu_btn = Button(WIDTH//2 - 80, HEIGHT//2 + 95, 150, 40, "Main Menu", BLUE, (0, 0, 150))
            
            personal_best = db.get_personal_best(username)
            
            while True:
                for e in pygame.event.get():
                    if e.type == pygame.QUIT:
                        return "quit"
                    if retry_btn.handle_event(e):
                        return "retry"
                    if menu_btn.handle_event(e):
                        return "menu"
                
                screen.fill(BLACK)
                game.draw(screen)
                
                overlay = pygame.Surface((WIDTH, HEIGHT))
                overlay.set_alpha(180)
                overlay.fill(BLACK)
                screen.blit(overlay, (0, 0))
                
                game_over_text = font_big.render("GAME OVER", True, RED)
                score_text = font_small.render(f"Score: {game.score}", True, WHITE)
                level_text = font_small.render(f"Level: {game.level}", True, WHITE)
                
                screen.blit(game_over_text, (WIDTH//2 - game_over_text.get_width()//2, HEIGHT//2 - 100))
                screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, HEIGHT//2 - 40))
                screen.blit(level_text, (WIDTH//2 - level_text.get_width()//2, HEIGHT//2 - 10))
                
                if personal_best:
                    pb_text = font_small.render(f"Best: {personal_best}", True, WHITE)
                    screen.blit(pb_text, (WIDTH//2 - pb_text.get_width()//2, HEIGHT//2 + 20))
                
                retry_btn.draw(screen)
                menu_btn.draw(screen)
                
                pygame.display.flip()
                clock.tick(60)
        
        pygame.display.flip()
        clock.tick(game.speed)

def main():
    settings = Settings()
    db = Database()
    db.setup_tables()
    
    current_screen = "menu"
    username = None
    
    while True:
        if current_screen == "menu":
            result, data = main_menu(settings, db)
            if result == "quit":
                break
            elif result == "play":
                username = data
                current_screen = "game"
            elif result == "leaderboard":
                current_screen = "leaderboard"
            elif result == "settings":
                if data is not None:
                    settings = data
                current_screen = "menu"
        
        elif current_screen == "leaderboard":
            result = leaderboard_screen(db)
            if result == "quit":
                break
            elif result == "menu":
                current_screen = "menu"
        
        elif current_screen == "game":
            result = game_loop(username, settings, db)
            if result == "quit":
                break
            elif result == "menu":
                current_screen = "menu"
            elif result == "retry":
                current_screen = "game"
    
    db.close()
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()