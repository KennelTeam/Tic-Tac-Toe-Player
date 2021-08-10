from typing import *
from utils.player_role import PlayerRole
import numpy as np


# true if step is correct
def validate_step(field: np.ndarray, step: Tuple[int, int]) -> bool:
    if 0 <= step[0] < field.shape[0] and 0 <= step[1] < field.shape[1]:
        return field[step[0]][step[1]] == 0
    return False


# true if tie
def check_tie(field: np.ndarray) -> bool:
    for line in field:
        for point in line:
            if point == 0:
                return False
    return False


def revert_field(field: np.ndarray) -> np.ndarray:
    return field * -1


def check_game_result(field: np.ndarray, last_step: Tuple[int, int], last_player: PlayerRole) -> PlayerRole:
    print(field.transpose())
    empty = np.zeros(field.shape)

    for dx in [-1, 0, 1]:
        for dy in [0, 1]:
            if (dx == 0 and dy == 0) or (dx == 1 and dy == 0):
                continue

            x, y = last_step
            print(x, y, dx, dy)
            print(validate_step(empty, (x, y)))

            while validate_step(empty, (x, y)) and abs(x - last_step[0]) < 5 and abs(y - last_step[1]) < 5:
                print(x, y, '--', sep=' ', end=', ')
                x -= dx
                y -= dy

            x += dx
            y += dy

            max_in_row = 0
            row = 0
            print('iterating: ', end=' ')
            while validate_step(empty, (x, y)) and abs(x - last_step[0]) < 5 and abs(y - last_step[1]) < 5:
                print(x, y, sep=' ', end=', ')
                if field[x][y] == 1 or (x, y) == last_step:
                    row += 1
                    max_in_row = max(max_in_row, row)
                else:
                    row = 0

                x += dx
                y += dy

            print()
            if max_in_row >= 5:
                return last_player

    if check_tie(field):
        return PlayerRole.TIE
    else:
        return PlayerRole.NONE
