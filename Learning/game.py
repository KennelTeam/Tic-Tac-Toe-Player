from utils.config import DEVICE_NAME
from utils.player_role import PlayerRole
from utils.step_validation import validate_step, check_game_result, revert_field
import typing
import torch
import numpy as np


class Game:

    FIELD_SIZE = 15

    def __init__(self):
        # list of tuples (x_step, y_step)
        self.steps_list: typing.List[typing.Tuple[int, int]] = list()
        self.end = False
        self.field = torch.zeros([1, self.FIELD_SIZE ** 2], device=torch.device(DEVICE_NAME))
        self.turn = PlayerRole.CROSSES
        self.winner = PlayerRole.NONE

    def set_field(self, x: int, y: int, value: int):
        self.field[0][x * self.FIELD_SIZE + y] = value

    def get_field(self, x, y):
        return self.field[0][x * self.FIELD_SIZE + y]

    def step(self, xy_step: typing.Tuple[int, int]):
        if self.end:
            raise RuntimeError("Attempt to make step after game is finished")
        if validate_step(self.field, xy_step):
            self.steps_list.append(xy_step)

            self.winner = check_game_result(self.field, xy_step, self.turn)
            self.set_field(xy_step[0], xy_step[1], 1)

            if self.winner != PlayerRole.NONE:
                self.end = True

            self.turn = PlayerRole.CROSSES if self.turn == PlayerRole.NOUGHTS else PlayerRole.NOUGHTS
            self.field = revert_field(self.field)
        else:
            raise RuntimeError("Attempt to make invalid step at coordinates {}".format(xy_step))

    def end_game(self) -> bool:
        return self.end

    def is_tie(self) -> bool:
        return self.winner == PlayerRole.TIE

    def get_winner(self) -> PlayerRole:
        return self.winner

    # generator function
    def get_steps(self) -> typing.Generator[typing.Tuple[torch.Tensor, typing.Tuple[int, int]], None, None]:
        field_tmp = torch.zeros([1, self.FIELD_SIZE ** 2], device=torch.device(DEVICE_NAME))

        for step in self.steps_list:
            yield field_tmp, step
            field_tmp[0][step[0] * self.FIELD_SIZE + step[1]] = 1
            field_tmp = revert_field(field_tmp)
