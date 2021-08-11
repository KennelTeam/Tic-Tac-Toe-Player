from NNStructure.base_facade import BaseFacade
from Learning.game import Game
from utils.player_role import PlayerRole
from utils.gameplay import play
import random
from datetime import datetime
from typing import *
import Statistics.stats
import threading


class Learning:

    K_CHECKPOINTS = 10

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

    def learn(self) -> Generator[PlayerRole, None, None]:
        chp_number = 1
        for ep in range(self.epochs):
            for winner in self.epoch():
                yield winner
            if ep / self.epochs >= 1 / self.K_CHECKPOINTS * chp_number:
                for player in self.players:
                    player.create_checkpoint(chp_number)
            random.shuffle(self.players)

    def epoch_async(self) -> Generator[PlayerRole, None, None]:
        threads = []
        for i in range(0, len(self.players), 2):
            first_player = self.players[i]
            second_player = self.players[min(i + 1, len(self.players) - 1)]
            thread = threading.Thread(target=Learning.play, args=(self, first_player, second_player))
            thread.start()
            threads.append(thread)

        for thread in threads:
            thread.join()
            yield PlayerRole.NONE

    def epoch(self) -> Generator[PlayerRole, None, None]:
        for first_player in self.players:
            for second_player in self.players:
                # print(first_player.cdir, second_player.cdir)
                game = self.play(first_player, second_player)
                yield game.get_winner()

    def play(self, crosses_player: BaseFacade, noughts_player: BaseFacade) -> Game:
        game = play(crosses_player, noughts_player)
        crosses_player.learn(game, PlayerRole.CROSSES)
        noughts_player.learn(game, PlayerRole.NOUGHTS)
        return game
