import json
import os
import random
from tqdm import tqdm

from Learning.game import Game
from NNStructure.simple_neuro.facade import SimpleNeuroFacade
from utils.player_role import PlayerRole
os.chdir('TicTacToe')
print(os.getcwd())
batch_size = 10
print('Starting reading')
gamesJson = json.loads(open('C:/Users/alexe/Documents/Hackatons/TicTacToe/data.json').read())
net = SimpleNeuroFacade(name='N1')
print('Starting learning')
for batch_index in tqdm(range(len(gamesJson) // batch_size)):
    batch = gamesJson[batch_index * batch_size: (batch_index + 1) * batch_size]
    structGames = []
    for gameJ in batch:
        g = Game()
        for step in gameJ:
            g.step(step)
        structGames.append(g)
    for game in structGames:
        role = PlayerRole.CROSSES
        if random.randint(0, 1) == 0:
            role = PlayerRole.NOUGHTS
        net.learn(game, role)
