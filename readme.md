# Tic-Tac-Toe-Player

`This is a neural network that should be able to play tic-tac-toe on big field`

## Installation

`git clone https://github.com/KennelTeam/tic-tac-toe-player`

`pip install -r requirements.txt`  
Run `main.py`

## Net learning

Learning process works through CLI

To start learning call `learn`. Parameters are:

- `-e <number of epochs> : integer`
- `-p <number of players (neural networks)> : integer`
- `--default <default NN Facade name to use if it is not set> : string`
- `--names <names of neural networks> : string as json list`
- `--show_statistics : print to show statistics at the end of process`
- `--warning_level <none | warnings | fatal>`

## What is lying under the hood?

Originally NN should learn by playing with each other but we had problems with speed (learning process was extremly slow and we couldn't figure out why) so eventually NN were learning on Renju games database [from here](http://www.renju.net/downloads/games.php)

### Program consists of modules:

- _NNStructure_ - Neural Networks are stored here. Each NN lies in personal directory and consists of 2 files:
  - _Struct_ - class, inherited from torch.nn.Module where structure of NN is stored
  - _Facade_ - class, inherited from _BaseFacade_ and implements methods to play games and learn
- _NNLoader_ - loads NN by it's name
- _Learning_ - plays learning-games among NNs and provides learning on renju games functionality
- _SaveGame_ - saves and loads games
- _CLI_ - reads commands and runs learning process
- _Visual_ - provides functionality to choose 2 NNs and play a demo-game (without learning) among them. Module visualizes games in user-friendly format

## Results we achieved

We have trained networks on renju games database so networks are not doing absurd decisions during ~15-20 first turns

But NNs cannot see patterns in game (such as 3 or 4 in a row) and can't really compete with person

## Problems

- The main problem we faced is the speed of learning - despite we use GPU and we have very little layers' size networks are learning extremly slow so we didn't have ability to our hypothesis

## Our hypothesis

which we didn't test enough =(

- Train networks by playing battles among them
- Train networlks on renju games database
- Apply precomputations such as searching for 3 and 4 in a row patterns on the field
