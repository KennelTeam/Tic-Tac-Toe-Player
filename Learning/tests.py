import pytest
from Learning.learning import Learning
from Learning.test_utils.test_facade import Facade1
from Learning.game import Game
from utils.player_role import PlayerRole


def test_learning_and_game():
    learner = Learning(Facade1, 5, 10)
    learner.learn()

def test_game_tie():
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
    print(game.field)
    assert game.end_game()
    assert game.get_winner() == PlayerRole.TIE


def test_game_not_tie():
    game = Game()
    steps_list = (0, 2, 1, 3, 4, 6, 5, 7, 8, 10, 9, 11, 12, 14, 13)
    for x in range(14):
        for y in steps_list:
            assert not game.end_game()
            game.step((x, y))
    # In last row:
    # +0+0+0
    # +0+0+0+
    # +0+0+0+       0
    # +0+0+0++      0
    # +0+0+0++     00
    # +0+0+0+++    00
    # +0+0+0+++   000
    # +0+0+0++++  000
    # +0+0+0++++ 0000
    # +0+0+0+++++0000
    for y in (0, 1, 2, 3, 4, 5, 6, 14, 7, 13, 8, 12, 9, 11, 10):
        assert not game.end_game()
        game.step((14, y))
    print(game.field)
    assert game.end_game()
    assert game.get_winner() == PlayerRole.CROSSES


def test_making_dirs():
    learner = Learning(Facade1, 5, 1)
