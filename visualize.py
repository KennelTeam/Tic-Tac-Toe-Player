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

index = int(input("Введите индекс игры: \n"))

game = Game()
for step in gamesJson[index]:
    game.step(step)
GameWindow(game)
