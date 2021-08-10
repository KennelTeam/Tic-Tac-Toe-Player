from typing import Tuple

import numpy as np
import torch

from NNStructure.base_facade import BaseFacade


class Neuro1Facade(BaseFacade):
    def make_move(self, field: np.ndarray) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        res = np.array()

    def learn(self, field: Tuple[tuple], correct: (int, int)):
        pass
