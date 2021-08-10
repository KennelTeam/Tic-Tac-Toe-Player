from typing import Tuple
from utils.player_role import PlayerRole
import numpy as np
from Learning.game import Game
from typing import Tuple
import torch

from NNStructure.base_facade import BaseFacade


class Neuro1Facade(BaseFacade):
    def make_move(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        pass

    def learn(self, game_history: Game, your_role: PlayerRole):
        for game_state in game_history.get_steps():
            pass
