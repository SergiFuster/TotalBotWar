import time

from Game.GUI.GUI import GUI
from Game.GameState import GameState
from Game.Action import Action


class Game:
    def __init__(self, parameters):
        self.game_state = GameState(parameters)
        self.reset()
        self.gui = GUI(parameters.screen_size, "TotalBotWar")  # Just for pygame version

    def reset(self):
        """Reset GameState so is ready for a new 'Game'"""
        self.game_state.reset()

    def run(self, l_players, forward_model,
            verbose: bool, budged: float, debug: bool, hud: bool):
        """Runs a TotalBotWar 'Game'"""
        for unit in self.game_state.player_0_units:
            print(unit, "\n")
        print("--------------------------------------------------------")
        for unit in self.game_state.player_1_units:
            print(unit, "\n")

        last_time = time.time()

        while not self.game_state.is_terminal:

            if verbose:
                time.sleep(0.01)
                self.gui.draw_screen(self.game_state.player_0_units +
                                     self.game_state.player_1_units,
                                     debug, hud)  # Just for pygame version

            if time.time() - last_time >= 0.1:
                for player in l_players:
                    observation = self.game_state.get_observation()
                    action = player.think(observation, budged)
                    forward_model.process_action(self.game_state, action)
                    last_time = time.time()
            forward_model.step(self.game_state)
