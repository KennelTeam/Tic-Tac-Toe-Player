import json
import shutil
import time

import numpy as np
import torch
import os
from torch import nn

from Learning.game import Game
from NNStructure.base_facade import BaseFacade
from NNStructure.simple_neuro.struct import SimpleNeuroStruct
from utils.config import DEVICE_NAME
from utils.player_role import PlayerRole


class SimpleNeuroFacade(BaseFacade):
    loss_function: nn.BCELoss
    cdir: str
    net: SimpleNeuroStruct

    def __init__(self, name: str, load_state=True, lr: float = 0.3):
        super().__init__(name)
        self.net = SimpleNeuroStruct()

        self.loss_function = nn.BCELoss()
        self.lr = lr

        exneuros = os.listdir('./Models')
        self.cdir = './Models/' + name + '/'
        if name in exneuros:
            config = self.load_config()
            if config['facade_name'] == self.__class__.__name__:
                if load_state:
                    if 'actual_state' in config.keys():
                        statePath = self.cdir + 'checkpoints/' + config['actual_state']
                        self.net = torch.load(statePath)
                        self.net.eval()

            else:
                raise RuntimeError('Facade in neuro config is different')
        else:
            os.mkdir("Models/" + name)
            os.mkdir("Models/" + name + '/checkpoints')
            shutil.copy('Models/stats_template.csv', self.cdir + 'stats.csv')
            config = {'name': name, 'facade_name': self.__class__.__name__}
            self.save_config(config)

        self.net = self.net.to(torch.device(DEVICE_NAME))
        # self.net.cuda(0)

    def net_learn(self):
        self.net.train()

    def net_play(self):
        self.net.eval()

    def load_config(self) -> dict:
        configFile = open(self.cdir + 'config.json')
        config = json.loads(configFile.read())
        configFile.close()
        return config

    def save_config(self, config: dict):
        configFile = open(self.cdir + 'config.json', 'w')
        configFile.write(json.dumps(config))
        configFile.close()

    def update_config(self, field: str, val):
        config = self.load_config()
        config[field] = val
        self.save_config(config)

    def create_checkpoint(self, index: int):
        fname = 'chp' + str(index) + '.pth.tar'
        torch.save(self.net, self.cdir + 'checkpoints/' + fname)
        self.update_config('actual_state', fname)

    def make_move(self, field: torch.Tensor) -> (int, int):
        best = ((-1, -1), -10)

        for i in range(15):
            for j in range(15):
                # fc = field.copy()
                if field[0][i * 15 + j] == 0:
                    field[0][i * 15 + j] = 1
                    r = self.net(field).item()
                    if r > best[1]:
                        best = ((i, j), r)
                    field[0][i * 15 + j] = 0

        return best[0]

    # legacy!!!
    def prepare_field(self, field: np.ndarray) -> torch.Tensor:
        res = np.zeros((1, 225), dtype='f')
        for i, val in enumerate(np.nditer(field)):
            res[0, i] = val
        result = torch.tensor(res, device=torch.device(DEVICE_NAME))
        return result

    def learn(self, game_history: Game, myrole: PlayerRole):
        isMyTurn = myrole == PlayerRole.CROSSES
        iWin = game_history.get_winner() == myrole
        if iWin:
            for field, inp_ans in game_history.get_steps():
                if isMyTurn:
                    # field = self.prepare_field(field)
                    for i in range(15):
                        for j in range(15):
                            # fc = field.copy()
                            if field[0][i * 15 + j] == 0:
                                field[0][i * 15 + j] = 1
                                if i == inp_ans[0] and j == inp_ans[1]:
                                    self.one_learning_step(field, True)
                                else:
                                    self.one_learning_step(field, False)
                                field[0][i * 15 + j] = 0
                isMyTurn = not isMyTurn

    def one_learning_step(self, field: torch.Tensor, isgood: bool):
        # field = self.prepare_field(field)
        field = field.to(torch.device(DEVICE_NAME))
        output = self.net(field)
        p2 = torch.tensor([[float(isgood)]], device=torch.device(DEVICE_NAME))
        loss = self.loss_function(output, p2)

        loss.backward()

        return loss, output
