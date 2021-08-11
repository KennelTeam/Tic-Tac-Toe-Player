from Visual.game_window import GameWindow
from Learning.game import Game
from utils.player_role import PlayerRole

game = Game()
steps_list = (0, 2, 1, 3, 4, 6, 5, 7, 8, 10, 9, 11, 12, 14, 13)
for x in range(15):
    for y in steps_list:
        assert not game.end_game()
        if game.field.sum() == 0:
            assert game.turn == PlayerRole.CROSSES
        else:
            assert game.turn == PlayerRole.NOUGHTS
        game.step((x, y))

GameWindow(game)
