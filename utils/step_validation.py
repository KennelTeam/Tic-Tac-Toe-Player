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
    for dx in [-1, 0, 1]:
        for dy in [0, 1]:
            if dx == 0 and dy == 0:
                continue

            coefficient_start = min(min(4, last_step[0] / dx if dx != 0 else 4),
                                    min(4, last_step[1] / dy if dy != 0 else 4))
            coefficient_end = min(min(4, ((field.shape[0] - last_step[0]) / dx) if dx != 0 else 4),
                                  min(4, ((field.shape[1] - last_step[1]) / dy) if dy != 0 else 4))

            max_in_row = 0
            row = 0

            for coefficient in range(coefficient_start, coefficient_end + 1):
                    x = last_step[0] + dx * coefficient
                    y = last_step[1] + dy * coefficient
                    if field[x][y] == 1:
                        row += 1
                        max_in_row = max(max_in_row, row)
                    else:
                        row = 0
            if max_in_row >= 5:
                return last_player

    if check_tie(field):
        return PlayerRole.TIE
    else:
        return PlayerRole.NONE
