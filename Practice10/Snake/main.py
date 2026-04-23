from tkinter import Tk, Canvas
from snake import Game

root = Tk()
root.title("Snake Game")

CELL_SIZE = 20
GRID_SIZE = 30

canvas_size = CELL_SIZE * GRID_SIZE

canvas = Canvas(root, width=canvas_size, height=canvas_size, bg="black")
canvas.pack()

game = Game(canvas, CELL_SIZE, GRID_SIZE)

root.mainloop()