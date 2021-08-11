# Нейронка, которая будет играть в крестики-нолики
## Установка
`git clone https://github.com/KennelTeam/tic-tac-toe-player`  
`pip install -r requirements.txt`  
Запускайте `main.py`

## Обучение нейросетей
Обучение нейросетей работает через консольный интерфейс
Для вызова функции обучения используйте команду `learn`
Ее параметры такие:  
`-e <number of epochs> : integer`  
`-p <number of players (neural networks)> : integer`  
`--default <default NN Facade name to use if it is not set> : string`  
`--names <names of neural networks> : string as json list`  
`--show_statistics : print to show statistics at the end of process`  
`--warning_level <none | warnings | fatal>`
## Правила работы с репозиторием
Лёва пушит в slave, остальные - в master
