import pygame
import sys
from random import randrange, choices
from db import Database
import time

CELL_SIZE = 20
GRID_SIZE = 30
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (139, 0, 0)
FOOD_COLORS = {
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0)
}

class Game:
    def __init__(self, username, settings, db):
        self.username = username
        self.settings = settings
        self.db = db
        
        self.snake = [[GRID_SIZE // 2, GRID_SIZE // 2]]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"
        
        self.obstacles = []
        self.food = None
        self.powerup = None
        self.active_effects = {}
        
        self.score = 0
        self.level = 1
        self.level_threshold = 5
        self.speed = 10
        self.clock = pygame.time.Clock()
        
        self.food_types = [
            {"color": "red", "weight": 1, "lifetime": 5000},
            {"color": "orange", "weight": 2, "lifetime": 3000},
            {"color": "yellow", "weight": 3, "lifetime": 2000},
        ]
        
        self.powerup_types = [
            {"name": "speed_boost", "color": (0, 255, 255), "duration": 5000, "effect": "boost"},
            {"name": "slow_motion", "color": (255, 255, 0), "duration": 5000, "effect": "slow"},
            {"name": "shield", "color": (0, 255, 255), "duration": 10000, "effect": "shield"}
        ]
        
        self.food_spawn_time = pygame.time.get_ticks()
        self.powerup_spawn_time = pygame.time.get_ticks()
        self.powerup_active_time = 0
        
        self.shield_active = False
        self.speed_multiplier = 1.0
        
        self.spawn_food()
        self.generate_obstacles()
    
    def draw_grid(self, screen):
        if self.settings.grid_overlay:
            for x in range(0, WIDTH, CELL_SIZE):
                pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
            for y in range(0, HEIGHT, CELL_SIZE):
                pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))
    
    def random_free_cell(self, avoid_snake=True):
        while True:
            cell = [randrange(0, GRID_SIZE), randrange(0, GRID_SIZE)]
            if avoid_snake and cell in self.snake:
                continue
            if cell in self.obstacles:
                continue
            if self.food and cell == self.food["pos"]:
                continue
            if self.powerup and cell == self.powerup["pos"]:
                continue
            return cell
    
    def spawn_food(self):
        current_time = pygame.time.get_ticks()
        food_type = choices(self.food_types, weights=[70, 20, 10])[0]
        self.food = {
            "pos": self.random_free_cell(),
            "color": food_type["color"],
            "weight": food_type["weight"],
            "spawn_time": current_time,
            "lifetime": food_type["lifetime"]
        }
        self.food_spawn_time = current_time
    
    def spawn_powerup(self):
        if not self.powerup and randrange(0, 100) < 15:
            powerup_type = choices(self.powerup_types)[0]
            self.powerup = {
                "pos": self.random_free_cell(),
                "name": powerup_type["name"],
                "color": powerup_type["color"],
                "duration": powerup_type["duration"],
                "effect": powerup_type["effect"],
                "spawn_time": pygame.time.get_ticks()
            }
            self.powerup_spawn_time = pygame.time.get_ticks()
    
    def generate_obstacles(self):
        if self.level >= 3:
            num_obstacles = min(5 + self.level // 2, 15)
            self.obstacles = []
            snake_head = self.snake[0]
            
            for _ in range(num_obstacles):
                while True:
                    obstacle = [randrange(0, GRID_SIZE), randrange(0, GRID_SIZE)]
                    if abs(obstacle[0] - snake_head[0]) < 3 and abs(obstacle[1] - snake_head[1]) < 3:
                        continue
                    if obstacle not in self.snake and obstacle not in self.obstacles:
                        self.obstacles.append(obstacle)
                        break
    
    def apply_powerup_effect(self, effect):
        current_time = pygame.time.get_ticks()
        if effect == "boost":
            self.speed_multiplier = 2.0
            self.active_effects["boost"] = current_time
        elif effect == "slow":
            self.speed_multiplier = 0.5
            self.active_effects["slow"] = current_time
        elif effect == "shield":
            self.shield_active = True
            self.active_effects["shield"] = current_time
    
    def update_powerup_effects(self):
        current_time = pygame.time.get_ticks()
        
        if "boost" in self.active_effects:
            if current_time - self.active_effects["boost"] > 5000:
                self.speed_multiplier = 1.0
                del self.active_effects["boost"]
        
        if "slow" in self.active_effects:
            if current_time - self.active_effects["slow"] > 5000:
                self.speed_multiplier = 1.0
                del self.active_effects["slow"]
        
        if "shield" in self.active_effects:
            if current_time - self.active_effects["shield"] > 10000:
                self.shield_active = False
                del self.active_effects["shield"]

        base_speed = 10 + (self.level - 1) * 2
        self.speed = int(base_speed * self.speed_multiplier)
        self.speed = max(5, min(30, self.speed))
    
    def move(self):
        self.direction = self.next_direction
        x, y = self.snake[0]
        
        if self.direction == "RIGHT":
            new_head = [x + 1, y]
        elif self.direction == "LEFT":
            new_head = [x - 1, y]
        elif self.direction == "UP":
            new_head = [x, y - 1]
        else:
            new_head = [x, y + 1]

        collision = (new_head in self.obstacles or
                    new_head[0] < 0 or new_head[0] >= GRID_SIZE or
                    new_head[1] < 0 or new_head[1] >= GRID_SIZE)
        
        if collision:
            if self.shield_active:
                self.shield_active = False
                if new_head[0] < 0:
                    new_head[0] = 0
                elif new_head[0] >= GRID_SIZE:
                    new_head[0] = GRID_SIZE - 1
                if new_head[1] < 0:
                    new_head[1] = 0
                elif new_head[1] >= GRID_SIZE:
                    new_head[1] = GRID_SIZE - 1
            else:
                self.save_game_result()
                return False
        
        if new_head in self.snake:
            if not self.shield_active:
                self.save_game_result()
                return False
        
        self.snake.insert(0, new_head)

        if new_head == self.food["pos"]:
            self.score += self.food["weight"]
            self.spawn_food()

            new_level = self.score // self.level_threshold + 1
            if new_level > self.level:
                self.level = new_level
                self.generate_obstacles()

        elif self.food.get("is_poison", False) and new_head == self.food["pos"]:
            for _ in range(2):
                if len(self.snake) > 1:
                    self.snake.pop()
            if len(self.snake) <= 1:
                self.save_game_result()
                return False
            self.spawn_food()
        else:
            self.snake.pop()
        
        if self.powerup and new_head == self.powerup["pos"]:
            self.apply_powerup_effect(self.powerup["effect"])
            self.powerup = None
        
        current_time = pygame.time.get_ticks()
        
        if current_time - self.food["spawn_time"] > self.food["lifetime"]:
            self.spawn_food()
        
        self.spawn_powerup()
        
        if self.powerup and current_time - self.powerup["spawn_time"] > 8000:
            self.powerup = None
        
        self.update_powerup_effects()
        
        return True
    
    def change_direction(self, new_dir):
        opposite = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if new_dir != opposite[self.direction]:
            self.next_direction = new_dir
    
    def save_game_result(self):
        self.db.save_game_result(self.username, self.score, self.level)
    
    def update(self):
        return self.move()
    
    def draw(self, screen):
        screen.fill(BLACK)
        self.draw_grid(screen)
        
        for x, y in self.obstacles:
            pygame.draw.rect(screen, GRAY, (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        fx, fy = self.food["pos"]
        time_left = self.food["lifetime"] - (pygame.time.get_ticks() - self.food["spawn_time"])
        color = FOOD_COLORS[self.food["color"]]
        if time_left < 1000:
            if (pygame.time.get_ticks() // 200) % 2 == 0:
                color = WHITE
        pygame.draw.rect(screen, color, (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        if self.powerup:
            px, py = self.powerup["pos"]
            pygame.draw.rect(screen, self.powerup["color"], 
                           (px * CELL_SIZE, py * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        for i, (x, y) in enumerate(self.snake):
            color = self.settings.snake_color
            if i == 0 and self.shield_active:
                color = (100, 100, 255)
            pygame.draw.rect(screen, color, 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(screen, (0, 0, 0), 
                           (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        font = pygame.font.SysFont("Arial", 24)
        text = font.render(f"Score: {self.score}  Level: {self.level}", True, WHITE)
        screen.blit(text, (5, 5))
        
        y_offset = 35
        if self.shield_active:
            shield_text = font.render("SHIELD ACTIVE", True, (100, 100, 255))
            screen.blit(shield_text, (5, y_offset))
            y_offset += 25
        if "boost" in self.active_effects:
            boost_text = font.render("SPEED BOOST", True, (0, 255, 255))
            screen.blit(boost_text, (5, y_offset))
            y_offset += 25
        if "slow" in self.active_effects:
            slow_text = font.render("SLOW MOTION", True, (255, 255, 0))
            screen.blit(slow_text, (5, y_offset))
        
        personal_best = self.db.get_personal_best(self.username)
        if personal_best:
            pb_text = font.render(f"Best: {personal_best}", True, WHITE)
            screen.blit(pb_text, (WIDTH - 150, 5))