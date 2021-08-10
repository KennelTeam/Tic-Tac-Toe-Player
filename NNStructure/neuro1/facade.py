from typing import Tuple

import numpy as np
from Learning.game import Game
from typing import Tuple
import torch

from NNStructure.base_facade import BaseFacade


class Neuro1Facade(BaseFacade):
    def make_move(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> (int, int):
        pass

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        res = np.array()

    def learn(self, game_history: Game):
        for game_state in game_history.get_steps():
            pass
