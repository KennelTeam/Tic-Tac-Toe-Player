from utils.player_role import PlayerRole
import typing


class Game:

    FIELD_SIZE = 15

    def __init__(self):
        self.steps_list = list()  # list of tuples (x_step, y_step)
        self.end = False
        self.field = [[0] * self.FIELD_SIZE for _ in range(self.FIELD_SIZE)]
        self.crosses_turn = True
        self.winner = PlayerRole.NONE

    def step(self, x_step: int, y_step: int):
        pass

    def end_game(self) -> bool:
        return self.end

    def is_drawn(self) -> bool:
        return self.end and self.winner == PlayerRole.NONE

    def winner(self) -> PlayerRole:
        return self.winner

    def get_steps(self) -> typing.Generator[list]:   # generator function
        while False:
            yield None
        raise StopIteration()
