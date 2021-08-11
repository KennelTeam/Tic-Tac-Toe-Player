from typing import *
from utils.player_role import PlayerRole
import numpy as np
import torch

FIELD_SIZE = 15


def validate_on_field(step: Tuple[int, int]) -> bool:
    return 0 <= step[0] < FIELD_SIZE and 0 <= step[1] < FIELD_SIZE


# true if step is correct
def validate_step(field: torch.Tensor, step: Tuple[int, int]) -> bool:
    if validate_on_field(step):
        return field[0][step[0] * FIELD_SIZE + step[1]] == 0
    return False


# true if tie
def check_tie(field: torch.Tensor) -> bool:
    return field.count_nonzero() == field.numel()


def revert_field(field: torch.Tensor) -> torch.Tensor:
    return field * -1


def check_game_result(field: torch.Tensor, last_step: Tuple[int, int], last_player: PlayerRole) -> PlayerRole:
    # return PlayerRole.NONE
    for dx in [-1, 0, 1]:
        for dy in [0, 1]:
            if (dx == 0 and dy == 0) or (dx == 1 and dy == 0):
                continue

            x, y = last_step
            while validate_on_field((x, y)) and abs(x - last_step[0]) < 5 and abs(y - last_step[1]) < 5:
                x -= dx
                y -= dy

            x += dx
            y += dy

            max_in_row = 0
            row = 0
            while validate_on_field((x, y)) and abs(x - last_step[0]) < 5 and abs(y - last_step[1]) < 5:
                if field[0][x * FIELD_SIZE + y] == 1 or (x, y) == last_step:
                    row += 1
                    max_in_row = max(max_in_row, row)
                else:
                    row = 0

                x += dx
                y += dy

            if max_in_row >= 5:
                return last_player

    field[0][last_step[0] * FIELD_SIZE + last_step[1]] = 1
    if check_tie(field):
        return PlayerRole.TIE
    else:
        return PlayerRole.NONE
