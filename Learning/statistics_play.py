from utils.gameplay import play
from NNLoader.nn_loader import load_nn
from utils.player_role import PlayerRole
import os
import re
import pandas as pd


def statistics_play(dir_name):
    versions = os.listdir(f'Models/{dir_name}/checkpoints')
    versions_sort = [(int(re.findall(r'chp(\d+)', v)[0]), v) for v in versions]
    versions_sort.sort()
    versions = [num_version for num_version, name in versions_sort]
    players = [load_nn(dir_name, version=version) for version in versions]
    stats = pd.DataFrame(columns=["Ties", "Wins", "Win rate"], index=versions, dtype=int)
    stats = stats.fillna(0)
    for idx_first, first_player in enumerate(players):
        vers_first = versions[idx_first]
        for idx_second, second_player in players:
            if idx_first == idx_second:
                continue
            vers_second = versions[idx_first + idx_second + 1]
            game = play(first_player, second_player)
            if game.is_tie():
                stats["Tie"][vers_first] += 1
                stats["Tie"][vers_second] += 1
            elif game.get_winner() == PlayerRole.CROSSES:
                stats["Wins"][vers_first] += 1
            else:
                stats["Wins"][vers_second] += 1
    games = (len(versions) - 1) * 2
    stats["Win rate"] = stats["Wins"] / games
    stats.to_csv(f'Models/{dir_name}/versions_stats.csv')

