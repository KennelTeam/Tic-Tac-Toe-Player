from utils.player_role import PlayerRole
from utils.step_validation import validate_step, check_game_result, revert_field
import typing


class Game:

    FIELD_SIZE = 15

    def __init__(self):
        # list of tuples (x_step, y_step)
        self.steps_list: typing.List[typing.Tuple[int, int]] = list()
        self.end = False
        self.field = [[0] * self.FIELD_SIZE for _ in range(self.FIELD_SIZE)]
        self.crosses_turn = True
        self.winner = PlayerRole.NONE

    def step(self, xy_step: typing.Tuple[int, int]):
        if self.end:
            raise RuntimeError("Attempt to make step after game is finished")
        if validate_step(self.field, xy_step):
            self.steps_list.append(xy_step)
            self.field[xy_step[0]][xy_step[1]] = 1
            self.winner = check_game_result(self.field, xy_step,
                                            PlayerRole.CROSSES if self.crosses_turn else PlayerRole.NOUGHTS)

            if self.winner != PlayerRole.NONE:
                self.end = True

            self.crosses_turn = not self.crosses_turn
            self.field = revert_field(self.field)
        else:
            raise RuntimeError("Attempt to make invalid step at coordinates {}".format(xy_step))

    def end_game(self) -> bool:
        return self.end

    def is_tie(self) -> bool:
        return self.winner == PlayerRole.TIE

    def get_winner(self) -> PlayerRole:
        return self.winner

    def get_steps(self) -> typing.Tuple[typing.Generator[typing.List[typing.List[int]]], int]:   # generator function
        field_tmp = [[0] * self.FIELD_SIZE for _ in range(self.FIELD_SIZE)]
        for step in self.steps_list:
            field_tmp[step[0]][step[1]] = 1
            yield field_tmp, step
            field_tmp = revert_field(field_tmp)
        raise StopIteration()
