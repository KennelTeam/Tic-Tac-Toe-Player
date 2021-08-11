from NNStructure.base_facade import BaseFacade
from Learning.game import Game
from utils.player_role import PlayerRole
import random
from datetime import datetime


class Learning:
    def __init__(self, model_class: type, players: int, epochs: int, dir_names=[]):
        self.model_class = model_class
        if len(dir_names) > players:
            raise RuntimeError("Too many directory names")
        if len(dir_names) != len(set(dir_names)):
            raise RuntimeError("Directory names are not unique")
        new_names = []
        for unnamed_counter in range(players - len(dir_names)):
            name = 'unnamed_' + \
                   str(datetime.now().strftime('%d.%m.%Y_%H:%M:%S_')) + str(unnamed_counter + 1)
            new_names.append(name)
            unnamed_counter += 1
        self.players = [model_class(dir_name) for dir_name in dir_names + new_names]
        self.epochs = epochs

    def learn(self):
        for ep in range(self.epochs):
            self.epoch()
            random.shuffle(self.players)

    def epoch(self):
        for idx, first_player in enumerate(self.players):
            for second_player in self.players[idx:]:
                self.play(first_player, second_player)
                self.play(second_player, first_player)

    def play(self, crosses_player: BaseFacade, noughts_player: BaseFacade):
        game = Game()
        while not game.end_game():
            if game.turn == PlayerRole.CROSSES:
                move = crosses_player.make_move(game.field)
            else:
                move = noughts_player.make_move(- game.field)
            game.step(move)
        crosses_player.learn(game, PlayerRole.CROSSES)
        noughts_player.learn(game, PlayerRole.NOUGHTS)
