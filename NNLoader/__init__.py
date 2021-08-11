import utils.nn_iterator
from NNStructure import base_facade
import os
import sys
import inspect
from typing import *

NN_FACADES: Dict[str, Type[base_facade.BaseFacade]] = {}
INITIALIZED = False
players = utils.nn_iterator.find_facades()
for name in players:
    path = "NNStructure." + name + ".facade"
    facade = __import__(path, fromlist=['object'])

    for class_name, obj in inspect.getmembers(facade):
        if inspect.isclass(obj) and inspect.getmodule(obj) == facade:
            if issubclass(obj, base_facade.BaseFacade):
                NN_FACADES[obj.__name__] = obj

INITIALIZED = True