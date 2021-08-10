import Visual.player
import typing


class UserPlayer(Visual.player.BasePlayer):
    def __init__(self, path: str, **kwargs):
        super().__init__()
        pass

    def make_move(self, field: typing.List[typing.List[int]]):
        pass

    def on_click(self, event):
        pass
