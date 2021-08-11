from NNStructure.base_facade import BaseFacade
from Learning.game import Game
from utils.player_role import PlayerRole
from utils.gameplay import play
import random
from datetime import datetime
from typing import *
import Statistics.stats


class Learning:
    def __init__(self, model_class: Type[BaseFacade], players: int, epochs: int, dir_names=[]):
        self.model_class = model_class
        if len(dir_names) > players:
            raise RuntimeError("Too many directory names")
        if len(dir_names) != len(set(dir_names)):
            raise RuntimeError("Directory names are not unique")
        new_names = []
        for unnamed_counter in range(players - len(dir_names)):
            name = 'unnamed_' + \
                   str(datetime.now().strftime('%d-%m-%Y_%H-%M-%S_')) + str(unnamed_counter + 1)
            new_names.append(name)
            unnamed_counter += 1

        self.players = []
        for dir_name in dir_names + new_names:
            self.players.append(model_class(dir_name))

        # self.players = [model_class(dir_name) for dir_name in dir_names + new_names]
        self.epochs = epochs

    def learn(self) -> Generator[Statistics.stats.StatsCompressed, None, None]:
        for ep in range(self.epochs):
            epoch_stats = self.epoch()
            random.shuffle(self.players)
            yield epoch_stats

    def epoch(self) -> Statistics.stats.StatsCompressed:
        for idx, first_player in enumerate(self.players):
            for second_player in self.players[idx:]:
                self.play(first_player, second_player)
                self.play(second_player, first_player)
        return Statistics.stats.StatsCompressed()

    def play(self, crosses_player: BaseFacade, noughts_player: BaseFacade) -> Game:
        print("a")
        game = play(crosses_player, noughts_player)
        print("b")
        crosses_player.learn(game, PlayerRole.CROSSES)
        print("c")
        noughts_player.learn(game, PlayerRole.NOUGHTS)
        print("d")
        return game
