from random import randrange, choice

class Game:
    def __init__(self, canvas, cell_size, grid_size):
        self.canvas = canvas
        self.cell_size = cell_size
        self.grid_size = grid_size
        self.base_speed = 150
        self.speed = self.base_speed
        self.snake = [[self.grid_size // 2, self.grid_size // 2]]
        self.walls = []
        self.food = self.spawn_food()
        self.score = 0
        self.direction = "Right"
        self.opposite = {
            "Up": "Down",
            "Down": "Up",
            "Left": "Right",
            "Right": "Left"
        }
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.set_direction)
        self.game_loop()

    def random_free_cell(self):
        while True:
            x = randrange(0, self.grid_size)
            y = randrange(0, self.grid_size)
            cell = [x, y]

            if cell not in self.snake and cell not in self.walls:
                return cell

    def spawn_food(self):
        return self.random_free_cell()

    def out_of_bounds(self, cell):
        x, y = cell
        return x < 0 or x >= self.grid_size or y < 0 or y >= self.grid_size

    def set_direction(self, event):
        if event.keysym in self.opposite:
            if event.keysym != self.opposite[self.direction]:
                self.direction = event.keysym

    def draw_grid(self):
        size = self.grid_size * self.cell_size
        for i in range(self.grid_size):
            x = i * self.cell_size
            self.canvas.create_line(x, 0, x, size, fill="#222")
            self.canvas.create_line(0, x, size, x, fill="#222")

    def draw(self):
        self.canvas.delete("all")
        self.draw_grid()
        cs = self.cell_size
        x, y = self.food
        self.canvas.create_rectangle(
            x*cs, y*cs, (x+1)*cs, (y+1)*cs,
            fill="red", width=0
        )
        for x, y in self.snake:
            self.canvas.create_rectangle(
                x*cs, y*cs, (x+1)*cs, (y+1)*cs,
                fill="green", width=0
        )
        self.canvas.create_text(
            5, 5,
            anchor="nw",
            text=f"Score: {self.score}",
            fill="white",
            font=("Arial", 14)
        )

    def compute_new_head(self):
        x, y = self.snake[0]
        if self.direction == "Right":
            return [x+1, y]
        elif self.direction == "Left":
            return [x-1, y]
        elif self.direction == "Up":
            return [x, y-1]
        else:
            return [x, y+1]

    def game_loop(self):
        self.draw()
        new_head = self.compute_new_head()
        if self.out_of_bounds(new_head) or new_head in self.snake:
            self.game_over()
            return
        self.snake.insert(0, new_head)
        if new_head == self.food:
            self.score += 1
            if self.speed > 60:
                self.speed -= 5
            self.food = self.spawn_food()
        else:
            self.snake.pop()
        self.canvas.after(self.speed, self.game_loop)

    def game_over(self):
        size = self.grid_size * self.cell_size
        self.canvas.create_text(
            size//2, size//2 - 20,
            text="GAME OVER",
            fill="white",
            font=("Arial", 24)
        )
        self.canvas.create_text(
            size//2, size//2 + 20,
            text=f"Score: {self.score}",
            fill="white",
            font=("Arial", 18)
        )