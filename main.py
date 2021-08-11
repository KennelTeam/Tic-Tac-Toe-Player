import pandas as pd
import matplotlib.pyplot as plt
from Visual.game_window import GameWindow

GameWindow()

statsPath = 'Models/t1/stats.csv'
open(statsPath)
data = pd.read_csv(statsPath)
data = data[['turns_in  _game', 'result', 'MSE']]
plt.plot(data)
plt.show()
