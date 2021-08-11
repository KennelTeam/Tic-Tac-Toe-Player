from typing import Tuple
from utils.config import DEVICE_NAME
import torch
from torch import nn


class SimpleNeuroStruct(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = [
            nn.Linear(225, 1, device=torch.device(DEVICE_NAME))
        ]
        for layer in self.layers:
            nn.init.uniform_(layer.weight, -1, 1)

    def forward(self, data: torch.Tensor) -> torch.Tensor:
        sm = nn.Sigmoid()
        for layer in self.layers:
            data = layer(data)
            data = sm(data)
        return data
