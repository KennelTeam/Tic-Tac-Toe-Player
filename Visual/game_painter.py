from Learning.game import Game
from utils.player_role import PlayerRole
import tkinter as tk
import typing


class GamePainter(Game):
    def __init__(self, canvas, canvas_size):
        super().__init__()
        self.canvas = canvas
        self.canvas_size = canvas_size

    def draw_cross(self, xy_step):
        x, y = xy_step
        x_coord, y_coord = (x + 1 / 3) * (self.canvas_size - 4) // 15, (y + 1 / 3) * (self.canvas_size - 4) // 15
        self.canvas.create_line(x_coord, y_coord, x_coord + 15, y_coord + 15, fill="red", width=2)
        self.canvas.create_line(x_coord + 15, y_coord, x_coord, y_coord + 15, fill="red", width=2)

    def draw_nought(self, xy_step):
        x, y = xy_step
        x_coord, y_coord = (x + 1 / 3) * (self.canvas_size - 4) // 15, (y + 1 / 3) * (self.canvas_size - 4) // 15
        self.canvas.create_oval(x_coord, y_coord, x_coord + 15, y_coord + 15, outline="blue", width=2)

    def draw_end_game(self):
        if self.is_tie():
            text_message = "TIE"
        elif self.get_winner() == PlayerRole.CROSSES:
            text_message = "CROSSES WON"
        else:
            text_message = "NOUGHTS WON"
        self.canvas.create_text(self.canvas_size // 2, self.canvas_size // 2,
                                text=text_message, justify=tk.CENTER, font="Verdana 40")

    def step(self, xy_step: typing.Tuple[int, int]):
        if self.turn == PlayerRole.CROSSES:
            self.draw_cross(xy_step)
        else:
            self.draw_nought(xy_step)
        super().step(xy_step)
        if self.end_game():
            self.draw_end_game()
