from typing import Tuple

import numpy as np
import torch
from torch import nn

from Learning.game import Game
from NNStructure.base_facade import BaseFacade
from NNStructure.simple_neuro.struct import SimpleNeuroStruct
from utils.player_role import PlayerRole


class SimpleNeuroFacade(BaseFacade):
    loss_function: nn.BCELoss
    optimizer: torch.optim.Adam

    def __init__(self, lr: float):
        super().__init__()
        self.net = SimpleNeuroStruct()
        self.loss_function = nn.BCELoss()
        self.lr = lr

    def net_learn(self):
        self.net.train()

    def net_play(self):
        self.net.eval()

    def make_move(self, field: np.ndarray) -> (int, int):
        best = ((-1, -1), -10)
        for i in range(15):
            for j in range(15):
                fc = field.copy()
                if fc[i][j] == 0:
                    fc[i][j] = 1
                    fc = self.prepare_field(fc)
                    r = round(self.net(fc).item())
                    if r > best[1]:
                        best = ((i, j), r)
        return best[0]

    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        res = np.zeros((1, 225), dtype='f')
        for i, val in enumerate(np.nditer(field)):
            res[0, i] = val
        return torch.tensor(res)

    def learn(self, game_history: Game, myrole: PlayerRole):
        isMyTurn = myrole == PlayerRole.CROSSES
        iWin = game_history.get_winner() == myrole
        if iWin:
            for field, inp_ans in game_history.get_steps():
                if isMyTurn:
                    for i in range(15):
                        for j in range(15):
                            fc = field.copy()
                            if fc[i][j] == 0:
                                fc[i][j] = 1
                                if i == inp_ans[0] and j == inp_ans[1]:
                                    self.one_learning_step(fc, True)
                                else:
                                    self.one_learning_step(fc, False)
                isMyTurn = not isMyTurn

    def one_learning_step(self, field: np.ndarray, isgood: bool):
        field = self.prepare_field(field)

        output = self.net(field)
        p2 = torch.tensor([[float(isgood)]])
        loss = self.loss_function(output, p2)

        loss.backward()

        return loss, output
