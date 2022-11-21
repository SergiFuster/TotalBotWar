import random
from Utilities.Vector import Vector


class Observation:
    def __init__(self, game_state):
        """
        Creates an observation with same data that game_state
        but randomize opponent units destinations cause is a hidden info
        :param game_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        """
        if game_state is not None:
            self.game_parameters = game_state.game_parameters.clone()
            self.player_0_units = self.clone_list_of_units(game_state.player_0_units)
            self.player_1_units = self.clone_list_of_units(game_state.player_1_units)
            self.is_terminal = game_state.is_terminal
            self.turn = game_state.turn

            if self.turn == 0:
                self.randomize_destinations(self.player_1_units)
            else:
                self.randomize_destinations(self.player_0_units)

    def clone_list_of_units(self, units):
        new_list = []

        for unit in units:
            new_list.append(unit.clone())

        return new_list

    def clone(self) -> "Observation":
        """
        Construct a new observation with same data but other references and return it
        :return: Observation
        """
        new_obs = Observation(self)
        new_obs.copy_random_destinations(self)
        return new_obs

    def copy_random_destinations(self, obs):
        if self.turn == 0:
            for i in range(len(self.player_1_units)):
                self.player_1_units[i].destination = obs.player_1_units[i].destination
        else:
            for i in range(len(self.player_0_units)):
                self.player_0_units[i].destination = obs.player_0_units[i].destination

    def randomize_destinations(self, units):
        """
        Randomize destinations of a list of TotalBotWar.Game.Unit.Unit elements
        :param units: List of TotalBotWar.Game.Unit.Unit
        :return: None
        """
        for unit in units:
            unit.destination = Vector([random.randrange(0, self.game_parameters.screen_size[0]),
                                      random.randrange(0, self.game_parameters.screen_size[1])])

    def get_unit_by_id_and_turn(self, id, turn=None):
        """
        Return unit with unit-id id and unit-team turn.
        turn is self-turn by default
        :param id: int
        :param turn: int
        :return: TotalBotWar.Game.Unit.Unit
        """
        if turn is None or turn < 0 or turn > 1:
            turn = self.turn

        return self.player_0_units[id] if turn == 0 else self.player_1_units[id]

    def get_units(self, turn=None):
        """
        Return list with units that belongs to turn
        If turn is None return units of self-turn
        :return: List of TotalBotWar.Game.Unit.Unit
        """
        if turn is None:
            turn = self.turn

        return self.player_0_units if turn == 0 else self.player_1_units
