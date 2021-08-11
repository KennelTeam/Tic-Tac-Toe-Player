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

    def test_init_facade(self):
        os.chdir('../')
        facade = SimpleNeuroFacade(lr=0.3, name='neuroX4')

    def test_update_config(self):
        os.chdir('../')
        facade = SimpleNeuroFacade(name='neuroX4', load_state=False)
        facade.update_config('actual_state', 'x2.pt')

    def test_create_checkpoint(self):
        os.chdir('../')
        facade = SimpleNeuroFacade(name='neuroX9', load_state=False)
        facade.create_checkpoint(1)
        facade2 = SimpleNeuroFacade(name='neuroX9')
        facade3 = SimpleNeuroFacade(name='neuroX10')
        self.assertTrue(torch.equal(facade.net.layers[0].weight, facade2.net.layers[0].weight))
        self.assertFalse(torch.equal(facade.net.layers[0].weight, facade3.net.layers[0].weight))
