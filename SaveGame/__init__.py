import pickle
from Learning.game import Game


def save_game(game: Game, filename='game1.pkl'):
    with open('Games/' + filename, 'wb') as file:
        pickle.dump(game, file, pickle.HIGHEST_PROTOCOL)


def import_game(filename='game1.pkl'):
    with open('Games/' + filename, 'rb') as file:
        game = pickle.load(file)
    return game
