import typing


class BasePlayer:
    def __init__(self):
        pass

    def make_move(self, field: typing.List[typing.List[int]]) -> typing.Tuple[int, int]:
        pass
