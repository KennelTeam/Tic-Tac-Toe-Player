import typing

class Game:

    FIELD_SIZE = 15

    def __init__(self):
        self.steps_list = list()  # list of tuples (x_step, y_step)
        self.end = False
        self.field = [[0] * self.FIELD_SIZE for _ in range(self.FIELD_SIZE)]
        self.crosses_turn = True

    def step(self, x_step: int , y_step: int):
        pass

    def end_game(self) -> bool:
        pass

    def is_drawn(self) -> bool:
        pass

    def is_crosses_won(self) -> bool:
        pass

    def get_steps(self) -> typing.Generator[list]:   # generator function
        while False:
            yield None
        raise StopIteration()