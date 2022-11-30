import time
import threading
from Game.GUI.GUI import GUI
from Game.GameState import GameState
from concurrent.futures import ThreadPoolExecutor

class Game:
    def __init__(self, parameters):
        self.game_state = GameState(parameters)
        self.reset()
        self.gui = GUI(self.game_state.game_parameters, "TotalBotWar")  # Just for pygame version
        self.pause = False      # Just for pygame version

    def reset(self):
        """Reset GameState so is ready for a new 'Game'"""
        self.game_state.reset()

    def request_actions(self, player, budged):
        while not self.game_state.is_terminal():
            if self.pause:
                continue
            time.sleep(0.1)
            observation = self.game_state.get_observation()
            t = time.time()
            action = player.think(observation, budged)
            t = time.time() - t
            print("Time expended {0} thinking: {1}".format(player, t))
            self.game_state.game_parameters.forward_model.process_action(self.game_state, action)

    def run(self, l_players,
            verbose, budged):
        """Runs a TotalBotWar 'Game'"""
        executor = ThreadPoolExecutor(max_workers=2)
        for unit in self.game_state.player_0_units:
            print(unit, "\n")
        print("--------------------------------------------------------")
        for unit in self.game_state.player_1_units:
            print(unit, "\n")

        self.game_state.game_parameters.set_start_time(time.time())
        executor.submit(self.request_actions, l_players[0], budged)
        executor.submit(self.request_actions, l_players[1], budged)
        while not self.game_state.is_terminal():

            time.sleep(1/self.game_state.game_parameters.frame_rate)
            if verbose:
                self.pause = self.gui.draw_screen(self.game_state.player_0_units +
                                                  self.game_state.player_1_units,
                                                  self.game_state.game_parameters.remaining_time)
            if self.pause:
                continue
            self.game_state.game_parameters.update_elapsed_time(time.time())  # Update times
            self.game_state.game_parameters.forward_model.step(self.game_state)
