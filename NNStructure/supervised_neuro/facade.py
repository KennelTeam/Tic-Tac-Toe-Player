import json
import shutil
import time

import numpy as np
import torch
import os
from torch import nn
import pandas as pd
from Learning.game import Game
from NNStructure.base_facade import BaseFacade
from NNStructure.supervised_neuro.struct import SupervisedNeuroStruct
from utils.config import DEVICE_NAME
from utils.player_role import PlayerRole


class SupervisedNeuroFacade(BaseFacade):
    loss_function: nn.BCELoss
    cdir: str
    net: SupervisedNeuroStruct
    statsTable: pd.DataFrame

    def __init__(self, name: str, load_state=True, lr: float = 0.00001, version: int = -1):
        super().__init__(name)
        self.net = SupervisedNeuroStruct()

        self.loss_function = nn.BCELoss()
        self.lr = lr

        exneuros = os.listdir('./Models')
        self.cdir = './Models/' + name + '/'
        if name in exneuros:
            config = self.load_config()
            if config['facade_name'] == self.__class__.__name__:
                if load_state:
                    if version == -1:
                        if 'actual_state' in config.keys():
                            statePath = self.cdir + 'checkpoints/' + config['actual_state']
                            self.net = torch.load(statePath)
                            self.net.eval()
                    else:
                        statePath = self.cdir + 'checkpoints/' + 'chp' + str(version) + '.pth.tar'
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
        self.statsTable = pd.read_csv(self.cdir + 'stats.csv')
        self.optimizer = torch.optim.Adam(self.net.parameters(), lr=self.lr)

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
        print("create_checkpoint")
        fname = 'chp' + str(index) + '.pth.tar'
        torch.save(self.net, self.cdir + 'checkpoints/' + fname)
        self.update_config('actual_state', fname)

    def make_move(self, field: torch.Tensor) -> (int, int):
        best = ((-1, -1), -10)
        field = self.prepare_field(field)

        for i in range(15):
            for j in range(15):
                # fc = field.copy()
                if field[0][i * 15 + j] == 0:
                    field[0][i * 15 + j] = 1
                    # field[0][225 + i * 15 + j] = 1
                    r = self.net(field).item()
                    if r >= best[1]:
                        best = ((i, j), r)
                    field[0][i * 15 + j] = 0
                    # field[0][225 + i * 15 + j] = 0

        return best[0]

    def prepare_field(self, field: torch.Tensor) -> torch.Tensor:
        # return torch.cat((field, torch.div((field + 1), 2), torch.div((field - 1), 2)), 1)
        return field

    def learn(self, game_history: Game, myrole: PlayerRole):
        # if myrole != game_history.get_winner():
        #     return
        iters = 1
        loss = 0
        corr_anses = 0
        for field, inp_ans in game_history.get_steps():
            field = self.prepare_field(field)
            for i in range(15):
                for j in range(15):
                    # fc = field.copy()
                    if field[0][i * 15 + j] == 0:
                        field[0][i * 15 + j] = 1
                        # field[0][225 + i * 15 + j] = 1
                        nloss = 0
                        iscnas = 0
                        if i == inp_ans[0] and j == inp_ans[1]:
                            nloss, iscans = self.one_learning_step(field, True)
                        else:
                            nloss, iscans = self.one_learning_step(field, False)

                        field[0][i * 15 + j] = 0
                        # field[0][225 + i * 15 + j] = 0

                        loss = (loss * iters + nloss) / (iters + 1)
                        corr_anses = (corr_anses * iters + iscnas) / (iters + 1)
                        iters += 1

    def one_learning_step(self, field: torch.Tensor, isgood: bool) -> (float, float):
        for param in self.net.parameters():
            param.grad = None

        output = self.net(field)
        p2 = torch.tensor([[float(isgood)]], device=torch.device(DEVICE_NAME))

        loss = self.loss_function(output, p2)
        loss.backward()

        self.optimizer.step()

        return loss, abs(round(float(isgood) - output.item()))
