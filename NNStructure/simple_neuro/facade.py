from typing import Tuple

import numpy as np
import torch

from NNStructure.base_facade import BaseFacade
from NNStructure.simple_neuro.struct import SimpleNeuroStruct


class SimpleNeuroFacade(BaseFacade):
    def __init__(self):
        super().__init__()
        self.net = SimpleNeuroStruct()

    def make_move(self, field: np.ndarray) -> (int, int):
        field = self.prepare_field(field)

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        res = np.zeros((225, 1), dtype='f')
        for i, val in enumerate(np.nditer(field)):
            res[i] = val
        return torch.tensor(res)

    def learn(self, field: Tuple[tuple], correct: (int, int)):
        pass
