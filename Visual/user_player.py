import _thread
import asyncio
import time
import tkinter

import numpy as np

from Learning.game import Game
from utils.player import BasePlayer
from utils.player_role import PlayerRole
import typing
import threading as thr
from tkinter import *


class UserPlayer(BasePlayer):
    __canvas: Canvas
    __canvas_size: int
    __role: PlayerRole
    __move: typing.Tuple[int, int] = None, None

    def __init__(self, canvas: Canvas, canvas_size: int, role: PlayerRole, step, **kwargs):
        super().__init__()
        self.__canvas = canvas
        self.__canvas_size = canvas_size
        self.__role = role
        self.__move_finished = IntVar()
        self.__step = step
        self.__canvas.bind("<Button-1>", self.on_click)
        self.waiting_move = thr.Event()

    def make_move(self, field: np.ndarray) -> typing.Tuple[int, int]:
        return self.__move

    def movvvve(self):
        print('wloop started')
        while not self.waiting_move.is_set():
            self.waiting_move.wait(60)
        print('wloop finished')
        return self.__move

    def on_click(self, event):
        print('clicked')
        x, y = event.x // (self.__canvas_size // 15), event.y // (self.__canvas_size // 15)
        if self.__role == PlayerRole.CROSSES:
            self.draw_cross(x, y)
        else:
            self.draw_nought(x, y)
        self.__move = x, y
        # self.__move_finished.set(1)
        self.waiting_move.set()
        self.__step(self.__move)

    def draw_cross(self, x, y):
        x_coord, y_coord = (x + 1 / 3) * (self.__canvas_size - 4) // 15, (y + 1 / 3) * (self.__canvas_size - 4) // 15
        self.__canvas.create_line(x_coord, y_coord, x_coord + 15, y_coord + 15, fill="red", width=2)
        self.__canvas.create_line(x_coord + 15, y_coord, x_coord, y_coord + 15, fill="red", width=2)

    def draw_nought(self, x, y):
        x_coord, y_coord = (x + 1 / 3) * (self.__canvas_size - 4) // 15, (y + 1 / 3) * (self.__canvas_size - 4) // 15
        self.__canvas.create_oval(x_coord, y_coord, x_coord + 15, y_coord + 15, outline="blue", width=2)
