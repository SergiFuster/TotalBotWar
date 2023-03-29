from Game.GameState import GameState
from Game.GameParameters import GameParameters
from Players.RandomPlayer import RandomPlayer
import json

gs = GameState(GameParameters([RandomPlayer(), RandomPlayer()]))
gs.reset()
json = json.dumps(gs.serialize())
print(json)
print("Número de bytes de un gamestate: ",len(json.encode()))
