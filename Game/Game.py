import time

from Game.GUI.GUI import GUI
from Game.GameState import GameState
from Game.Action import Action


class Game:
    def __init__(self, parameters):
        self.game_state = GameState(parameters)
        self.reset()
        self.gui = GUI(parameters.screen_size, "TotalBotWar")  # Just for pygame version
        self.pause = False      # Just for pygame version

    def reset(self):
        """Reset GameState so is ready for a new 'Game'"""
        self.game_state.reset()

    def run(self, l_players,
            verbose: bool, budged: float, debug: bool, hud: bool):
        """Runs a TotalBotWar 'Game'"""
        for unit in self.game_state.player_0_units:
            print(unit, "\n")
        print("--------------------------------------------------------")
        for unit in self.game_state.player_1_units:
            print(unit, "\n")

        last_time = time.time()

        while not self.game_state.is_terminal:
            time.sleep(1/self.game_state.game_parameters.frame_rate)
            t = time.time()
            if verbose:
                pause = self.gui.draw_screen(self.game_state.player_0_units +
                                             self.game_state.player_1_units,
                                             debug, hud)  # Just for pygame version

            if pause:
                continue
            t = time.time() - t
            print("Time expended drawing: ", t)

            if time.time() - last_time >= 0.1:
                for player in l_players:
                    observation = self.game_state.get_observation()
                    t = time.time()
                    action = player.think(observation, budged)
                    t = time.time() - t
                    print("Time expended player{0} thinking: {1}".format(player, t))
                    self.game_state.game_parameters.forward_model.process_action(self.game_state, action)
                    last_time = time.time()
            t = time.time()
            self.game_state.game_parameters.forward_model.step(self.game_state)
            t = time.time() - t
            print("Time expended stepping game: ", t)
