import torch
from torch import nn
from typing import Tuple
import numpy as np


class BaseFacade:
    def __init__(self):
        self.net = nn.Module()
        pass

    def make_move(self, field: np.ndarray) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        pass

    def learn(self, field: np.ndarray, correct: (int, int)):
        pass
