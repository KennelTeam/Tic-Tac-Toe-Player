from NNStructure import base_facade, NN_FACADES, INITIALIZED
import os
import json


def load_nn(name: str) -> base_facade.BaseFacade:
    if not INITIALIZED:
        raise RuntimeError("Module NNStructure should be initialized by importing it")
    path = os.path.join("Models", os.path.join(name, "config.json"))
    if os.path.exists(path) and os.path.isfile(path):
        raise RuntimeError(f"Incorrect name of NN: {name}")
    file = open(path, 'r')
    data = json.loads(''.join(file.readlines()))
    file.close()
    facade_name = data['facade_name']
    return NN_FACADES[facade_name](name)


