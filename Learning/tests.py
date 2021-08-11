import pytest
from Learning.learning import Learning
from Learning.test_utils.test_facade import Facade1


def test_learning():
    learner = Learning(Facade1, 5, 10)
    learner.learn()
