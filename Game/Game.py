import time
import func_timeout
from Game.GUI.GUI import GUI
from Game.GameState import GameState
from concurrent.futures import ThreadPoolExecutor


class Game:
    def __init__(self, parameters):
        self.game_state = GameState(parameters)
        self.reset()
        self.gui = GUI(self.game_state.game_parameters, "TotalBotWar")  # Just for pygame version
        self.pause = False      # Just for pygame version
        self.action_p0 = None
        self.action_p1 = None
        self.thread_p0_thinking = False
        self.thread_p1_thinking = False

    def reset(self):
        """Reset GameState so is ready for a new 'Game'"""
        self.game_state.reset()

    def player_0_thinking(self, observation, player, budged):

        self.thread_p0_thinking = True
        print(player, " thinking...")
        t = time.time()

        try:
            self.action_p0 = func_timeout.func_timeout(budged, player.think, args=[observation, budged])
            t = time.time() - t
        except func_timeout.FunctionTimedOut:
            print("{0} exceeded time to think, choosing random action...".format(player))
            self.action_p0 = observation.get_random_action()

        print("{0} time expended: {1}".format(player, t))
        self.thread_p0_thinking = False

    def player_1_thinking(self, observation, player, budged):

        self.thread_p1_thinking = True
        print(player, " thinking...")
        t = time.time()

        try:
            self.action_p1 = func_timeout.func_timeout(budged, player.think, args=[observation, budged])
            t = time.time() - t
        except func_timeout.FunctionTimedOut:
            print("{0} exceeded time to think, choosing random action...".format(player))
            self.action_p1 = observation.get_random_action()

        print("{0} time expended: {1}".format(player, t))
        self.thread_p1_thinking = False

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

        last_time = time.time()
        while not self.game_state.is_terminal():
            if verbose:
                self.pause = self.gui.draw_screen(self.game_state.player_0_units +
                                                  self.game_state.player_1_units,
                                                  self.game_state.game_parameters.remaining_time)
            if self.pause:
                continue

            if time.time() - last_time >= 0.1:
                if not self.thread_p0_thinking:
                    executor.submit(self.player_0_thinking, self.game_state.get_observation(0), l_players[0], budged)
                if not self.thread_p1_thinking:
                    executor.submit(self.player_1_thinking, self.game_state.get_observation(1), l_players[1], budged)
                last_time = time.time()

            if self.action_p0 is not None:
                self.game_state.game_parameters.forward_model.process_action(self.game_state, self.action_p0, 0)
                self.action_p0 = None

            if self.action_p1 is not None:
                self.game_state.game_parameters.forward_model.process_action(self.game_state, self.action_p1, 1)
                self.action_p1 = None

            self.game_state.game_parameters.update_elapsed_time(time.time())  # Update times
            self.game_state.game_parameters.forward_model.step(self.game_state)

        winner = self.game_state.get_winner()
        if winner != -1:
            finish_message = "{0} wins the game!".format(l_players[winner])
        else:
            finish_message = "It's a draw NO ONE WINS"
        while True:
            self.gui.draw_final_screen(finish_message)
