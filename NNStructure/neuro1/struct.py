from typing import Tuple

from torch import nn


class Neuro1Struct(nn.Module):
    def __init__(self, layers_size: Tuple[int]):
        super().__init__()
        self.layers = []
        for i in range(len(layers_size)-1):
            self.layers.append(nn.Linear(layers_size[i], layers_size[i+1]))

    def forward(self, data: Tuple[float]):
        for layer in self.layers:
            data = layer(data)
        return data
