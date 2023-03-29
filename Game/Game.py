import json
import time
import func_timeout
from Game.ForwardModel import ForwardModel
from Game.GameState import GameState
from concurrent.futures import ThreadPoolExecutor
from Game.Action import Action
from Players.HumanPlayer import HumanPlayer
from Utilities.Vector import Vector


class Game:
    def __init__(self, parameters):
        self.game_state = GameState(parameters)
        self.reset()
        self.action_p0 = None
        self.action_p1 = None
        self.thread_p0_thinking = False
        self.thread_p1_thinking = False
        self.human_playing = -1
        self.forward_model = ForwardModel()

    def reset(self):
        """Reset GameState so is ready for a new 'Game'"""
        self.game_state.reset()

    def player_0_thinking(self, observation, player, budged):

        self.thread_p0_thinking = True
        # print(player, " thinking...")
        try:
            self.action_p0 = func_timeout.func_timeout(budged, player.think, args=[observation, budged])
        except func_timeout.FunctionTimedOut:
            # print("{0} exceeded time to think, choosing random action...".format(player))
            self.action_p0 = observation.get_random_action()
        self.thread_p0_thinking = False

    def player_1_thinking(self, observation, player, budged):
        self.thread_p1_thinking = True
        # print(player, " thinking...")
        try:
            self.action_p1 = func_timeout.func_timeout(budged, player.think, args=[observation, budged])
        except func_timeout.FunctionTimedOut:
            # print("{0} exceeded time to think, choosing random action...".format(player))
            self.action_p1 = observation.get_random_action()
        self.thread_p1_thinking = False

    def run(self, l_players,
            verbose, budged, socket):
        """Runs a TotalBotWar 'Game'"""

        if isinstance(l_players[0], HumanPlayer):
            self.human_playing = 0

        elif isinstance(l_players[1], HumanPlayer):
            self.human_playing = 1

        executor = ThreadPoolExecutor(max_workers=2)

        self.game_state.game_parameters.set_start_time(time.time())

        last_time = time.time()

        # region INFORMATION
        timer = time.time()
        fps = frames = seconds = 0
        # endregion

        # Wait client message for start the game loop (client is doing the setup for it's game)
        message = socket.change_information(self.game_state)
        # Finish execution inmediatly if message received is not "START"
        """if message.decode() != "START": 
            self.finish_game("Error with start message", socket)
            return"""

        # region MAIN LOOP
        while not self.game_state.is_terminal():

            input = socket.change_information(self.game_state)
            time_loop = time.time()
            # region INFORMATION

            if time.time() - timer >= 1:
                timer = time.time()
                frames += fps
                seconds += 1
                if verbose:
                    print(f"Fps = {fps}, total frames = {frames}, \taverage fps: {frames / seconds:.1f}")
                fps = 0
            else:
                fps += 1
            # endregion

            if self.human_playing != -1 and isinstance(input, Vector):
                self.manage_input(input)

            if time.time() - last_time >= 0.1:

                # region THREADS
                if not self.thread_p0_thinking:
                    executor.submit(self.player_0_thinking, self.game_state.get_observation(0), l_players[0], budged)
                if not self.thread_p1_thinking:
                    executor.submit(self.player_1_thinking, self.game_state.get_observation(1), l_players[1], budged)

                # endregion

                # region NO THREADS
                # try:
                #    self.action_p0 = func_timeout.func_timeout(budged, l_players[0].think,
                #                                               args=[self.game_state.get_observation(0), budged])
                # except func_timeout.FunctionTimedOut:
                #    self.action_p0 = self.game_state.get_observation(0).get_random_action()
                #
                # try:
                #    self.action_p1 = func_timeout.func_timeout(budged, l_players[1].think,
                #                                               args=[self.game_state.get_observation(1), budged])
                # except func_timeout.FunctionTimedOut:
                #    self.action_p1 = self.game_state.get_observation(1).get_random_action()
                # endregion

                last_time = time.time()

            # region Actions Execution
            if self.action_p0 is not None:
                if verbose: print(f"Action p0 : {self.action_p0}")
                self.forward_model.process_action(self.game_state, self.action_p0, 0)
                self.action_p0 = None

            if self.action_p1 is not None:
                if verbose: print(f"Action p1 : {self.action_p0}")
                self.forward_model.process_action(self.game_state, self.action_p1, 1)
                self.action_p1 = None
            # endregion

            self.game_state.game_parameters.update_elapsed_time(time.time())  # Update times
            self.forward_model.step(self.game_state)
        # endregion

        winner = self.game_state.get_winner()

        if winner != -1:
            finish_message = f"{l_players[winner]} wins the game!"
        else:
            finish_message = "It's a draw NO ONE WINS"

        self.finish_game(finish_message, socket)

    def finish_game(self, finish_message, socket):
        socket.send_message(finish_message)

    def manage_input(self, input):
        """
        If no unit is selected, select it (no action to execute).
        Set action with unit selected and input position otherwise
        """
        units = self.game_state.player_0_units if self.human_playing == 0 else self.game_state.player_1_units
        selected = self.forward_model.some_unit_is_selected(units)
        if selected:
            # create action
            action = Action(selected, input.x, input.y)
            selected.selected = False
            if self.human_playing == 0:
                self.action_p0 = action
            else:
                self.action_p1 = action
        else:
            # select unit
            clicked = self.forward_model.unit_clicked(units, (input.x, input.y))
            if clicked:
                clicked.selected = True
