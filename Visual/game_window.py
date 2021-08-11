import asyncio
import os
import typing
from pathlib import Path
from tkinter import *
import tkinter
from tkinter import Canvas
from tkinter.ttk import Combobox

from Learning.game import Game
from utils import player
from typing import *
from utils.player_role import PlayerRole
from utils import gameplay
from user_player import UserPlayer
from nn_player import NNPlayer
import _thread

import tkinter as tk


# map player names to paths to config files
def find_players() -> Dict[str, str]:
    pass


class GameWindow(tk.Tk):
    __field: List[List[int]]
    __cross_player: player.BasePlayer
    __noughts_player: player.BasePlayer
    # map name of player (which will be rendered) to path to config file
    __player_options: Dict[str, str]
    __current_player: PlayerRole

    __tkinter_window = tkinter.Tk()

    __is_game_started: bool = False
    __is_game_finished: bool = False

    __field_size = 380
    __field_canvas = Canvas(width=__field_size, height=__field_size, background="gray")
    game: Game

    def __init__(self, crosses_player: player.BasePlayer, noughts_player: player.BasePlayer):
        super().__init__()
        self.__crosses_player = crosses_player
        self.__noughts_player = noughts_player

        self.__tkinter_window.geometry("700x500")

        first_player = Combobox(self.__tkinter_window)
        second_player = Combobox(self.__tkinter_window)
        start_button = Button(self.__tkinter_window, text="Start", command=self.event_catcher())

        neuros_list = os.listdir(str(Path(os.getcwd()).parent) + "\Models")
        neuros_list.insert(0, "User")
        first_player["values"], second_player["values"] = neuros_list, neuros_list
        first_player.current(0)
        second_player.current(0)
        self.__field_canvas.grid(column=1, row=1, padx=10, pady=10)
        first_player.grid(column=0, row=0)
        start_button.grid(column=1, row=0)
        second_player.grid(column=2, row=0)
        # self.__field_canvas.bind("<Button-1>", self.click_on_field_1)
        # self.__field_canvas.bind("<Button-3>", self.click_on_field_2)
        self.__field_canvas.focus_set()

        for x in range(4, self.__field_size, self.__field_size // 15):
            self.__field_canvas.create_line(x, 4, x, self.__field_size)

        for y in range(4, self.__field_size, self.__field_size // 15):
            self.__field_canvas.create_line(4, y, self.__field_size, y)

    def event_catcher(self):
        print('got event')
        self.start_game()

    def start_game(self):
        print('game started')
        self.game = Game()

        crosses_player = UserPlayer(self.__field_canvas, self.__field_size, PlayerRole.CROSSES, self.step)
        noughts_player = UserPlayer(self.__field_canvas, self.__field_size, PlayerRole.NOUGHTS, self.step)
        while not self.game.end_game():
            if self.game.turn == PlayerRole.CROSSES:
                crosses_player.make_move(self.game.field)
            else:
                noughts_player.make_move(self.game.field)
            # game.step(move)
        return self.game

    def step(self, move: typing.Tuple[int, int]):
        self.game.step(move)

    # def click_on_field_1(self, event):
    #     self.draw_cross(event.x // (self.__field_size // 15), event.y // (self.__field_size // 15))
    #
    # def click_on_field_2(self, event):
    #     self.draw_nought(event.x // (self.__field_size // 15), event.y // (self.__field_size // 15))
    #
    # def draw_cross(self, x, y):
    #     x_coord, y_coord = (x + 1 / 3) * (self.__field_size - 4) // 15, (y + 1 / 3) * (self.__field_size - 4) // 15
    #     self.__field_canvas.create_line(x_coord, y_coord, x_coord + 15, y_coord + 15, fill="red", width=2)
    #     self.__field_canvas.create_line(x_coord + 15, y_coord, x_coord, y_coord + 15, fill="red", width=2)
    #
    # def draw_nought(self, x, y):
    #     x_coord, y_coord = (x + 1 / 3) * (self.__field_size - 4) // 15, (y + 1 / 3) * (self.__field_size - 4) // 15
    #     self.__field_canvas.create_oval(x_coord, y_coord, x_coord + 15, y_coord + 15, outline="blue", width=2)


game_window = GameWindow(player.BasePlayer(), player.BasePlayer())
game_window.mainloop()
