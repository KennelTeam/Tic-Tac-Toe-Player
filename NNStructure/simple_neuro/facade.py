import json
import shutil

import numpy as np
import torch
import os
from torch import nn

from Learning.game import Game
from NNStructure.base_facade import BaseFacade
from NNStructure.simple_neuro.struct import SimpleNeuroStruct
from utils.player_role import PlayerRole


class SimpleNeuroFacade(BaseFacade):
    loss_function: nn.BCELoss
    cdir: str
    net: SimpleNeuroStruct

    def __init__(self, name: str, load_state=True, lr: float = 0.3):
        super().__init__(name)
        self.net = SimpleNeuroStruct()
        self.net.cuda()
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
