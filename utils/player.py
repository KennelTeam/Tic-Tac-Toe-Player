import typing
import numpy as np


class BasePlayer:
    def __init__(self):
        pass

    def make_move(self, field: np.ndarray) -> typing.Tuple[int, int]:
        pass
