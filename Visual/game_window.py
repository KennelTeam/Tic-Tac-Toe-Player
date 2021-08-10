import tkinter
from Visual import player
from typing import *
from utils.player_role import PlayerRole

# map player names to paths to config files
def find_players() -> Dict[str, str]:
    pass


class GameWindow:
    __field: List[List[int]]
    __cross_player: player.BasePlayer
    __noughts_player: player.BasePlayer
    # map name of player (which will be rendered) to path to config file
    __player_options: Dict[str, str]
    __current_player: PlayerRole

    __tkinter_window: tkinter.Tk

    __is_game_started: bool = False
    __is_game_finished: bool = False

    def __init__(self, crosses_player: player.BasePlayer, noughts_player: player.BasePlayer, window: tkinter.Tk):
        self.__crosses_player = crosses_player
        self.__noughts_player = noughts_player
        self.__tkinter_window = window
        pass

    def render(self) -> None:
        pass

    def check_win(self) -> bool:
        pass

    def on_move_done(self, move: Tuple[int, int]):
        pass

    def on_game_started(self):
        pass
