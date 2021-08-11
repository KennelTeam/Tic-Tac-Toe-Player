import pandas as pd
import matplotlib.pyplot as plt

statsPath = 'C:/Users/alexe/Documents/Hackatons/TicTacToe/Models/t1/stats.csv'
open(statsPath)
data = pd.read_csv(statsPath)
data = data[['turns_in  _game', 'result', 'MSE']]
plt.plot(data)
plt.show()
