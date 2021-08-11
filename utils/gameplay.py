from Learning.game import Game
from utils.player_role import PlayerRole
from utils.player import BasePlayer
import time


def play(crosses_player: BasePlayer, noughts_player: BasePlayer) -> Game:
    game = Game()
    spent_time = 0
    steps = 0

    begin_total = time.time()
    while not game.end_game():
        steps += 1
        if game.turn == PlayerRole.CROSSES:
            begin = time.time()
            move = crosses_player.make_move(game.field)
            end = time.time()
            spent_time += end - begin
        else:
            begin = time.time()
            move = noughts_player.make_move(game.field)
            end = time.time()
            spent_time += end - begin
        game.step(move)
    end_total = time.time()
    print(f"avg time: {spent_time / steps}")
    print(f"total spent: {spent_time}")
    print(f"total: {end_total - begin_total}")
    return game
