from Learning.game import Game
from utils.player_role import PlayerRole
from NNStructure.base_facade import BaseFacade
import numpy as np
import os


class Facade1(BaseFacade):
    def __init__(self, dir_name):
        super().__init__()
        self.dir_name = dir_name
        if dir_name not in os.listdir('Models'):
            os.mkdir('Models/' + dir_name)

    def make_move(self, field: np.ndarray):
        for x in range(len(field)):
            for y in range(len(field)):
                if field.sum() == 0:
                    if field[x, y] == 0:
                        print(">>", x, y)
                        return x, y
                else:
                    if field[y, x] == 0:
                        print(">>>", y, x)
                        return y, x

    def prepare_field(self, field: np.ndarray):
        pass

    def learn(self, game_history: Game, your_role: PlayerRole):
        print("Learn!!")
        print("PlayerRole:", "CROSSES" if your_role == PlayerRole.CROSSES else "NOUGHTS")
        if game_history.get_winner() == your_role:
            print("I won!")
        elif game_history.is_tie():
            print("Tie :|")
        else:
            print("I lost :(")