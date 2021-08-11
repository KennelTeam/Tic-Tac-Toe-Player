import torch
from torch import nn
from typing import Tuple
from Learning.game import Game
from utils.player_role import PlayerRole
from utils.player import BasePlayer
import numpy as np


class BaseFacade(BasePlayer):
    def __init__(self, name: str):
        super().__init__()
        self.net = nn.Module()
        pass

    def make_move(self, field: np.ndarray) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        pass

    def learn(self, game_history: Game, your_role: PlayerRole):
        pass
