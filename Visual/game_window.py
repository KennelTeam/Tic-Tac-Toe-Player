import os
import typing
from pathlib import Path
from tkinter import *
import tkinter
from tkinter import Canvas
from tkinter.ttk import Combobox

from utils.nn_iterator import find_players
from NNLoader.nn_loader import load_nn
from Learning.game import Game
from Visual.game_painter import GamePainter
from typing import *
from utils.player_role import PlayerRole


class GameWindow:
    __field: List[List[int]]
    # map name of player (which will be rendered) to path to config file
    __player_options: Dict[str, str]
    __current_player: PlayerRole

    __tkinter_window = tkinter.Tk()

    __is_game_started: bool = False
    __is_game_finished: bool = False
    __is_user_turn: bool = False

    __field_size = 380
    __field_canvas = Canvas(width=__field_size, height=__field_size, background="gray")
    game: Game

    def __init__(self):
        self.__crosses_player = None
        self.__noughts_player = None
        self.__tkinter_window.geometry("700x500")

        self.first_player = Combobox(self.__tkinter_window)
        self.second_player = Combobox(self.__tkinter_window)
        start_button = Button(self.__tkinter_window, text="Start", command=self.start_game)

        neuros_list = list(find_players().values())
        neuros_list.insert(0, "User")
        self.first_player["values"], self.second_player["values"] = neuros_list, neuros_list
        self.first_player.current(0)
        self.second_player.current(0)
        self.__field_canvas.grid(column=1, row=1, padx=10, pady=10)
        self.first_player.grid(column=0, row=0)
        start_button.grid(column=1, row=0)
        self.second_player.grid(column=2, row=0)
        self.__field_canvas.bind("<Button-1>", self.click_on_field)
        self.__field_canvas.focus_set()

        for x in range(4, self.__field_size, self.__field_size // 15):
            self.__field_canvas.create_line(x, 4, x, self.__field_size)

        for y in range(4, self.__field_size, self.__field_size // 15):
            self.__field_canvas.create_line(4, y, self.__field_size, y)

        self.__tkinter_window.mainloop()

    def click_on_field(self, event):
        if not self.__is_game_started:
            return
        if not self.__is_user_turn:
            return
        cell_size = self.__field_size // 15
        x_cell = event.x // cell_size
        y_cell = event.y // cell_size
        self.game.step((x_cell, y_cell))
        self.__tkinter_window.update()
        if not self.game.end_game():
            self.step()


    def start_game(self):
        self.__is_game_started = True
        self.game = GamePainter(self.__field_canvas, self.__field_size)
        self.__crosses_player = self.first_player.get()
        self.__noughts_player = self.second_player.get()
        if self.__crosses_player != "User":
            self.__crosses_player = load_nn(self.__crosses_player)
        if self.__noughts_player != "User":
            self.__noughts_player = load_nn(self.__noughts_player)

        self.step()

    def step(self):
        cur_player = self.__crosses_player if self.game.turn == PlayerRole.CROSSES else self.__noughts_player
        if cur_player == "User":
            self.__is_user_turn = True
            return
        self.__is_user_turn = False
        step_xy = cur_player.make_move(self.game.field)
        self.game.step(step_xy)
        self.__tkinter_window.update()

        if not self.game.end_game():
            self.step()
