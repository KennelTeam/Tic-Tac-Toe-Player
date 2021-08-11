from NNStructure.base_facade import BaseFacade
from Learning.game import Game
from utils.player_role import PlayerRole
import random


class Learning:
    def __init__(self, model_class: type, players: int, epochs: int, **kwargs):
        self.model_class = model_class
        self.players = [model_class() for _ in range(players)]  # list of players those are model_class typed
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

    def play(self, crosses_player: BaseFacade, noughts_player: BaseFacade) -> Game:
        game = Game()
        while not game.end_game():
            if game.turn == PlayerRole.CROSSES:
                move = crosses_player.make_move(game.field)
            else:
                move = noughts_player.make_move(- game.field)
            game.step(move)
        crosses_player.learn(game, PlayerRole.CROSSES)
        noughts_player.learn(game, PlayerRole.NOUGHTS)
