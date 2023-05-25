import sys
import json
from Network.SocketManager import SocketTCP
from Players.RandomPlayer import RandomPlayer
from Players.OSLAPlayer import OSLAPlayer
from Players.HumanPlayer import HumanPlayer
from Heuristics.SimpleHeuristic import SimpleHeuristic
from Game.Game import Game
from Game.GameParameters import GameParameters
"""
This is de module used to start an instance of the game.

This file will always be initialized by father process
it will pass a series of parameters, that parameters will be the next.

Parameters:
    1. File name
    2. Host direction (socket connection)
    3. Port (socket connection)
    4. Client id
    5. Bot 1 name
    6. Bot 2 name

Total parameters count: 6

"""


def player_from_string(player_string):
    player_string = player_string.lower()
    if "osla" in player_string:
        return OSLAPlayer(SimpleHeuristic())
    elif "human" in player_string:
        return HumanPlayer()
    else:
        return RandomPlayer()


def send_father_message(message, tries=10):
    """
    Perform sending message for process creator by standard output
    :param message: String
    :param tries: Int
    :return: Bool
    """
    if tries < 0: return False
    try:
        print(message)
        sys.stdout.flush()
    except sys.stdout.errors as e:
        return send_father_message(message, tries - 1)
    return True


if len(sys.argv) != 8:
    # Try to send the message 5 times
    send_father_message("ERROR", 5)
    sys.exit()

HOST, PORT, CLIENT_ID, bot0String, bot1String, screen_width, screen_height = sys.argv[1], \
                                                                             sys.argv[2], \
                                                                             sys.argv[3], \
                                                                             sys.argv[4], \
                                                                             sys.argv[5], \
                                                                             sys.argv[6], \
                                                                             sys.argv[7]

socket = SocketTCP(HOST, PORT)

# Try to connect, return message with the result to the father
connected, message = socket.connect()
send_father_message(message)

# And kill this process if mandatory
if not connected: sys.exit()

# Wait client for 10 seconds
if not socket.wait_client(CLIENT_ID, 10):
    sys.exit()

# Create bots according to BOT1 and BOT2
bot0 = player_from_string(bot0String)
bot1 = player_from_string(bot1String)

# Get Initial Positions
initial_positions = socket.receive_initial_positions()
if initial_positions is not None:
    initial_positions = json.loads(initial_positions)

verbose = False
budged = 3
players = [bot0, bot1]
screen_size = (int(screen_width), int(screen_height))
game_parameters = GameParameters(players, screen_size, initial_positions)
game = Game(game_parameters)
game.run(players, verbose, budged, socket)
socket.close()
sys.exit()


