from Game.Game import Game
from Game.GameParameters import GameParameters
from Players.RandomPlayer import RandomPlayer
from Players.OSLAPlayer import OSLAPlayer
from Heuristics.SimpleHeuristic import SimpleHeuristic
from Players.HumanPlayer import HumanPlayer
from Players.AlwaysStraightPlayer import AlwaysStraightPlayer
from Players.AlwaysStoppedPlayer import AlwaysStoppedPlayer

LINE = "-----------------------------------------------------------------------------"

"""units = list()
units.append(Unit(Type.SWORD, 1, 100, 100))
units.append(Unit(Type.HORSE, 2, 200, 100))
units.append(Unit(Type.SPEAR, 3, 300, 100))
units.append(Unit(Type.BOW, 4, 400, 100))

print("UNITS BEFORE MODIFICATIONS: ")
for unit in units:
    print()
    unit.test()

print(LINE)

print("UNITS BUFFED * 1.5: ")
for unit in units:
    unit.modify_stats(lambda x: x*1.5)
    print()
    unit.test()

print(LINE)

print("UNITS WITH ATTRIBUTES RESTORED: ")
for unit in units:
    unit.restore_stats()
    print()
    unit.test()

print(LINE)

print("TESTING EXCEPTIONS CREATING UNITS")
try:
    units.append(Unit("hulahula", 123, 0, 0))
except Exception as e:
    print(e)

print(LINE)

print("TESTING ACTION CLASS")

action1 = Action(units[0].id, units[0].x, units[0].y)
action2 = Action(units[0].id, units[0].x, units[0].y)
action3 = Action(units[1].id, units[1].x, units[1].y)

print("Action1 == Action2: ", action1 == action2)
print("Action1 == Action3: ", action1 == action3)
print("Action1 == units[0]: ", action1 == units[0])"""

verbose = True
budged = 3
players = [OSLAPlayer(SimpleHeuristic()), RandomPlayer()]
game_parameters = GameParameters(players)
game = Game(game_parameters)
game.run(players, verbose, budged)



