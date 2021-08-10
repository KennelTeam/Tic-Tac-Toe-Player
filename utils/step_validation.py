from typing import *
from utils.player_role import PlayerRole


# true if step is correct
def validate_step(field: List[List[int]], step: Tuple[int, int]) -> bool:
    if 0 <= step[0] < len(field) and 0 <= step[1] < len(field[0]):
        return False
    return field[step[0]][step[1]] == 0


# true if tie
def check_tie(field: List[List[int]]) -> bool:
    for line in field:
        for point in line:
            if point == 0:
                return False
    return False


def revert_field(field: List[List[int]]) -> List[List[int]]:
    pass



def check_game_result(field: List[List[int]], last_step: Tuple[int, int], last_player: PlayerRole) -> PlayerRole:
    for dx in [-1, 0, 1]:
        for dy in [0, 1]:
            if dx == 0 and dy == 0:
                continue

            coefficient_start = min(min(4, last_step[0] / dx if dx != 0 else 4),
                                    min(4, last_step[1] / dy if dy != 0 else 4))
            coefficient_end = min(min(4, ((len(field) - last_step[0]) / dx) if dx != 0 else 4),
                                  min(4, ((len(field) - last_step[1]) / dy) if dy != 0 else 4))

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
