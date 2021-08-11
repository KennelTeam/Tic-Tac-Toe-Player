from typing import Tuple
from utils.config import DEVICE_NAME
import torch
from torch import nn


class SupervisedNeuroStructure(nn.Module):
    def __init__(self):
        super(SupervisedNeuroStructure, self).__init__()
        self.fc1 = nn.Linear(225, 1024, device=torch.device(DEVICE_NAME))
        self.fc2 = nn.Linear(1024, 1024, device=torch.device(DEVICE_NAME))
        self.fc3 = nn.Linear(1024, 1, device=torch.device(DEVICE_NAME))

        nn.init.uniform_(self.fc1.weight, -1, 1)
        nn.init.uniform_(self.fc2.weight, -1, 1)
        nn.init.uniform_(self.fc3.weight, -1, 1)
        print("self.parameters:")
        for p in self.parameters():
            print(p)
        print("end self.parameters")

    def forward(self, data: torch.Tensor) -> torch.Tensor:
        sm = nn.Sigmoid()
        data = self.fc1(data)
        data = sm(data)
        data = self.fc2(data)
        data = sm(data)
        data = self.fc3(data)
        data = sm(data)
        return data
