class Observation:
    def __init__(self, game_state: "TotalBotWar.Game.GameState.GameState"):
        if game_state is not None:
            self.game_parameters = game_state.game_parameters
            self.player_0_units = game_state.player_0_units
            self.player_1_units = game_state.player_1_units
            self.is_terminal = game_state.is_terminal
            self.turn = game_state.turn

    def clone(self) -> "Observation":
        """
        Construct a new observation with same data but other references and return it
        :return: Observation
        """
        new_observation = Observation(None)
        new_observation.game_parameters = self.game_parameters
        new_observation.player_0_units = self.player_0_units[:]
        new_observation.player_1_units = self.player_1_units[:]
        new_observation.is_terminal = self.is_terminal
        new_observation.turn = self.turn
        return new_observation

    def get_units(self):
        """
        :return: list of units of player turn by value
        """
        return self.player_0_units[:] if self.turn == 0 else self.player_1_units[:]
