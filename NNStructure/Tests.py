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
