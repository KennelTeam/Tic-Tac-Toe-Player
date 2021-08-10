import torch
from torch import nn
from typing import Tuple
import numpy as np


class BaseFacade:
    def __init__(self):
        self.net = nn.Module()
        pass

    def make_move(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> torch.Tensor:
        pass

    def learn(self, field: np.ndarray(shape=(15, 15), dtype=np.float), correct: (int, int)):
        pass
