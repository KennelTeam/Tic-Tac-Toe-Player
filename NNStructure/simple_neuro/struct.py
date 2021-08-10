from typing import Tuple

import torch
from torch import nn


class SimpleNeuroStruct(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = [
            nn.Linear(225, 225)
        ]

    def forward(self, data: torch.Tensor) -> torch.Tensor:
        for layer in self.layers:
            data = layer(data)
        return data
