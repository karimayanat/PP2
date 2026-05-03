DB_CONFIG = {
    "host": "127.0.0.1",
    "port": "5433",
    "database": "snake_game",
    "user": "postgres",
    "password": "12345"
}

CELL_SIZE = 20
GRID_SIZE = 30
WIDTH = CELL_SIZE * GRID_SIZE
HEIGHT = CELL_SIZE * GRID_SIZE

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0)
GRAY = (128, 128, 128)
DARK_GRAY = (64, 64, 64)
BLUE = (0, 0, 255)

INITIAL_SPEED = 10
LEVEL_THRESHOLD = 5