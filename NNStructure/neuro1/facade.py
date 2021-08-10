from typing import Tuple

import numpy as np

from NNStructure.base_facade import BaseFacade


class Neuro1Facade(BaseFacade):
    def make_move(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> (int, int):
        pass

    def learn(self, field: Tuple[tuple], correct: (int, int)):
        pass
