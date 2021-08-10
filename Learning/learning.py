from NNStructure.base_facade import BaseFacade
from Learning.game import Game


class Learning:
    def __init__(self, model_class: type, players: int, epochs: int, **kwargs):
        self.model_class = model_class
        self.players = [None for _ in range(players)]  # list of players those are model_class typed
        self.epochs = epochs

    def learn(self):
        pass

    def epoch(self):
        pass

    def play(self, crosses_player: BaseFacade, noughts_player: BaseFacade) -> Game:
        pass

    def save_players_state(self):
        pass

    def save_statistics(self, **kwargs):
        pass
