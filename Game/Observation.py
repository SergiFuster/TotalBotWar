import random
from Utilities.Vector import Vector
from Game.Action import Action


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

    def copy_into(self, other_observation):
        """
        Copy information from self to other_observation
        This is optimal than make a clone
        :param other_observation: TotalBotWar.Game.Observation.Observation
        :return: None
        """
        self.copy_list_of_players(self.player_0_units, other_observation.player_0_units)
        self.copy_list_of_players(self.player_1_units, other_observation.player_1_units)
        other_observation.is_terminal = self.is_terminal
        other_observation.turn = self.turn
        self.copy_random_destinations(other_observation)

    def copy_list_of_players(self, list_units_1, list_units_2):
        """
        Copy data from list_units_1 to list_units_2
        :param list_units_1: List of TotalBotWar.Game.Unit.Unit
        :param list_units_2: List of TotalBotWar.Game.Unit.Unit
        :return: None
        """

        # We are sure that both lists are equal sized
        for i in range(len(list_units_1)):
            list_units_1[i].copy_into(list_units_2[i])

    def get_macro_actions(self, h=4, v=4):
        """
        For every unit that can move calculate its possible actions
        moving it to all portions of map, map is divided horizontally by h
        and vertically by v to reduce possibilities
        :param h: int optional
        :param v: int optional
        :return: List of TotalBotWar.Game.Action.Action
        """
        positions = self.get_portion_positions(h, v)
        actions = []
        if self.turn == 0:
            for unit in self.player_0_units:
                if unit.can_move():
                    for position in positions:
                        actions.append(Action(unit, position[0], position[1]))      # Available positions to move
                    actions.append(Action(unit, unit.position.x, unit.position.y))  # Stop the unit
        else:
            for unit in self.player_1_units:
                if unit.can_move():
                    for position in positions:
                        actions.append(Action(unit, position[0], position[1]))      # Available positions to move
                    actions.append(Action(unit, unit.position.x, unit.position.y))  # Stop the unit
        return actions

    def get_portion_positions(self, h, v):
        """
        Calculate the center of the positions of each portion
        :param h: int (horizontal portions)
        :param v: int (vertical portions)
        :return: List of tuples(x, y)
        """
        portion_h = self.game_parameters.screen_size[0] / h
        portion_v = self.game_parameters.screen_size[1] / v
        initial_v_pos = portion_v / 2
        h_pos = portion_h / 2   # Initial horizontal pos
        positions = []
        for hIndex in range(h):
            v_pos = initial_v_pos
            for vIndex in range(v):
                positions.append((h_pos, v_pos))
                v_pos += portion_v
            h_pos += portion_h
        return positions

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

    def get_units(self, available=False, turn=None):
        """
        Return list with units
        available to move
        If available is True, all units else
        that belongs to turn
        If turn is None, self-turn else
        :return: List of TotalBotWar.Game.Unit.Unit
        """
        if turn is None:
            turn = self.turn

        if not available:
            return self.player_0_units if turn == 0 else self.player_1_units

        available_units = []
        if turn == 0:
            for unit in self.player_0_units:
                if unit.can_move():
                    available_units.append(unit)
        else:
            for unit in self.player_1_units:
                if unit.can_move():
                    available_units.append(unit)
        return available_units

