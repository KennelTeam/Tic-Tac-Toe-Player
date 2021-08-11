from Learning.game import Game
from utils.player_role import PlayerRole
from utils.player import BasePlayer


def play(crosses_player: BasePlayer, noughts_player: BasePlayer) -> Game:
    game = Game()
    while not game.end_game():
        if game.turn == PlayerRole.CROSSES:
            move = crosses_player.make_move(game.field)
        else:
            move = noughts_player.make_move(game.field)
        game.step(move)
    return game
