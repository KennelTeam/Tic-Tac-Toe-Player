from typing import Tuple
from Learning.game import Game
import numpy as np

from NNStructure.base_facade import BaseFacade


class Neuro1Facade(BaseFacade):
    def make_move(self, field: np.ndarray(shape=(15, 15), dtype=np.float)) -> (int, int):
        pass

    def learn(self, game_history: Game):
        for game_state in game_history.get_steps():
            pass
