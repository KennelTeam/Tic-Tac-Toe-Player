import torch
from torch import nn
from typing import Tuple
from Learning.game import Game
from utils.player_role import PlayerRole
import numpy as np


class BaseFacade:
    def __init__(self):
        self.net = nn.Module()
        pass

    def make_move(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> torch.Tensor:
        pass

    def learn(self, game_history: Game, your_role: PlayerRole):
        pass
