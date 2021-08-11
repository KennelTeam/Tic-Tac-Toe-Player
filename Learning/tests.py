import pytest
from Learning.learning import Learning
from Learning.test_utils.test_facade import Facade1
from Learning.game import Game
import os
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
    assert game.is_tie()
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


def test_game_noughts_won():
    game = Game()
    steps_list = ((0, 0), (1, 0), (0, 2), (2, 1), (0, 3), (3, 2), (0, 4), (4, 3), (0, 5), (5, 4))
    for step in steps_list:
        assert not game.end_game()
        game.step(step)
    assert game.end_game()
    assert game.get_winner() == PlayerRole.NOUGHTS



def test_making_directories():
    if 'test_dir1' not in os.listdir('Models'):
        os.mkdir('Models/test_dir1')
    if 'test_dir2' in os.listdir('Models'):
        os.rmdir('Models/test_dir2')
    len_listdir = len(os.listdir('Models'))
    learner = Learning(Facade1, 5, 1, ['test_dir1', 'test_dir2'])
    assert 'test_dir1' in os.listdir('Models')
    assert 'test_dir2' in os.listdir('Models')
    print(len(os.listdir('Models')), len_listdir)
    assert len(os.listdir('Models')) == len_listdir + 4
    for pl in learner.players:
        os.rmdir('Models/' + pl.dir_name)
