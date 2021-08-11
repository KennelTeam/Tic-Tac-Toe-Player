class StatsCompressed:
    avg_steps_per_game: int = 5
    max_win_cnt: int = 30
    min_win_cnt: int = 2
    total_games: int = 47

    def __init__(self, avg_steps_per_game: int = 5, max_win_cnt: int = 30, min_win_cnt: int = 2, total_games = 47):
        self.avg_steps_per_game = avg_steps_per_game
        self.max_win_cnt = max_win_cnt
        self.min_win_cnt = min_win_cnt
        self.total_games = total_games

    def to_string(self) -> str:
        return f"""Average steps per game: {self.avg_steps_per_game}
Max win rate: {round(100 * self.max_win_cnt / self.total_games, 1)}%
Min win rate: {round(100 * self.min_win_cnt / self.total_games, 1)}%"""


class Stats(StatsCompressed):
    pass
