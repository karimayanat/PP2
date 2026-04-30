import pygame
import sys
from random import randrange, choices

CELL_SIZE = 20
GRID_SIZE = 30
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE
BLACK = (0, 0, 0)
GREEN = (0, 200, 0)
WHITE = (255, 255, 255)
FOOD_COLORS = {
    "red": (255, 0, 0),
    "orange": (255, 165, 0),
    "yellow": (255, 255, 0)
}

class Game:
    def __init__(self):
        self.snake = [[GRID_SIZE // 2, GRID_SIZE // 2]]
        self.direction = "RIGHT"
        self.next_direction = "RIGHT"

        self.food_types = [
            {"color": "red", "weight": 1},
            {"color": "orange", "weight": 2},
            {"color": "yellow", "weight": 3},
        ]
        self.food = self.spawn_food()
        self.score = 0
        self.level = 1
        self.level_threshold = 5
        self.speed = 10
        self.clock = pygame.time.Clock()

    def draw_grid(self, screen):
        for x in range(0, WIDTH, CELL_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, HEIGHT))
        for y in range(0, HEIGHT, CELL_SIZE):
            pygame.draw.line(screen, (40, 40, 40), (0, y), (WIDTH, y))

    def random_free_cell(self):
        while True:
            cell = [randrange(0, GRID_SIZE), randrange(0, GRID_SIZE)]
            if cell not in self.snake:
                return cell

    def spawn_food(self):
        food_type = choices(self.food_types, weights=[70, 20, 10])[0]
        return {
            "pos": self.random_free_cell(),
            "color": food_type["color"],
            "weight": food_type["weight"]
        }

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

        if (
            new_head in self.snake or
            new_head[0] < 0 or new_head[0] >= GRID_SIZE or
            new_head[1] < 0 or new_head[1] >= GRID_SIZE
        ):
            return False

        self.snake.insert(0, new_head)

        if new_head == self.food["pos"]:
            self.score += self.food["weight"]
            new_level = self.score // self.level_threshold + 1
            if new_level > self.level:
                self.level = new_level
                if self.level % 3 == 0:
                    self.speed += 2 

            self.food = self.spawn_food()
        else:
            self.snake.pop()

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

    def draw(self, screen, font):
        screen.fill(BLACK)
        self.draw_grid(screen)
        fx, fy = self.food["pos"]
        pygame.draw.rect(
            screen,
            FOOD_COLORS[self.food["color"]],
            (fx * CELL_SIZE, fy * CELL_SIZE, CELL_SIZE, CELL_SIZE)
        )
        for x, y in self.snake:
            pygame.draw.rect(
                screen,
                GREEN,
                (x * CELL_SIZE, y * CELL_SIZE, CELL_SIZE, CELL_SIZE)
            )
        text = font.render(f"Score: {self.score}  Level: {self.level}", True, WHITE)
        screen.blit(text, (5, 5))
        pygame.display.flip()

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Snake (pygame)")
    font = pygame.font.SysFont("Arial", 20)
    game = Game()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.change_direction("UP")
                elif event.key == pygame.K_DOWN:
                    game.change_direction("DOWN")
                elif event.key == pygame.K_LEFT:
                    game.change_direction("LEFT")
                elif event.key == pygame.K_RIGHT:
                    game.change_direction("RIGHT")

        alive = game.move()
        if not alive:
            print("GAME OVER. Score:", game.score)
            pygame.quit()
            sys.exit()

        game.draw(screen, font)
        game.clock.tick(game.speed)

if __name__ == "__main__":
    main()