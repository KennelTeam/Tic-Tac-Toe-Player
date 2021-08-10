from typing import Tuple

from torch import nn


class Neuro1Struct(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = []

    def forward(self, data: Tuple[float]):
        for layer in self.layers:
            data = layer(data)
        return data
