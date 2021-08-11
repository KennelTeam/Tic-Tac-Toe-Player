import unittest

import numpy as np

from NNStructure.simple_neuro.facade import *


class Tests(unittest.TestCase):

    def test_field_prepare(self):
        obj = SimpleNeuroFacade()
        field = np.zeros((15, 15), float)
        field[1][0] = 1
        field[0][1] = -1
        r = obj.prepare_field(field)
        self.assertEqual(len(r), 225)
        self.assertEqual(r[1], -1)
        self.assertEqual(r[15], 1)
        self.assertEqual(r[30], 0)

    def test_neuro(self):
        neuro = SimpleNeuroStruct()
        data = torch.tensor(np.zeros((1, 225), dtype='f'))
        r = neuro(data)
        # print(r)

    def test_one_learning_step(self):
        imax = -100
        imin = 100
        mloss = 0
        for _ in range(100):
            obj = SimpleNeuroFacade(lr=0.3)
            field = np.zeros((15, 15), float)
            field[1][0] = 1
            field[0][1] = -1
            correct = True
            loss, output = obj.one_learning_step(field, correct)
            if output < imin:
                imin = output
            if output > imax:
                imax = output
            # print(loss)
            # print(output)
            mloss += loss / 100
        # print(imin, imax, mloss)

    def test_learn(self):
        game = Game()
        game.step((7, 7))
        game.step((6, 6))
        game.step((8, 8))
        game.step((8, 9))
        game.step((9, 9))
        game.step((10, 10))
        game.step((10, 11))
        game.step((11, 11))
        tf = SimpleNeuroFacade(lr=0.3)
        tf.learn(game, PlayerRole.CROSSES)

    def test_make_move(self):
        moves = set()
        for _ in range(100):
            obj = SimpleNeuroFacade(lr=0.3)
            field = np.zeros((15, 15), float)
            field[1][0] = 1
            field[0][1] = -1
            move = obj.make_move(field)
            moves.add(move)
        print(moves)


