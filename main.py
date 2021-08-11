import json
import random
from tqdm import tqdm

from Learning.game import Game
from NNStructure.simple_neuro.facade import SimpleNeuroFacade
from utils.player_role import PlayerRole

batch_size = 10

gamesJson = json.loads(open('data.json').read())
net = SimpleNeuroFacade(name='N1')

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
