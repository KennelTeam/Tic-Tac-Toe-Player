import json
import os
import random
from tqdm import tqdm

from Learning.game import Game
from NNStructure.supervised_neuro.facade import SupervisedNeuroFacade
from NNStructure.simple_neuro.facade import SimpleNeuroFacade
from utils.player_role import PlayerRole
import time
from Visual.game_window import GameWindow

# os.chdir('TicTacToe')
print(os.getcwd())
batch_size = 1
print('Starting reading')
gamesJson = json.loads(open('data.json').read())
net = SupervisedNeuroFacade(name='sup7')
print('Starting learning')

for batch_index in tqdm(range(len(gamesJson) // batch_size)):
    begin_func = time.time()
    batch = gamesJson[batch_index * batch_size: (batch_index + 1) * batch_size]
    structGames = []
    begin_upload = time.time()
    print(begin_upload - begin_func)
    for gameJ in batch:
        g = Game()
        for step in gameJ:
            g.step(step)
        structGames.append(g)
    end_upload = time.time()
    for game in structGames:
        net.learn(game, PlayerRole.CROSSES)
        GameWindow(game)
    end_learning = time.time()
    print(end_upload - begin_upload)
    print(end_learning - end_upload)
    net.create_checkpoint(batch_index)
    print(time.time() - end_learning)
