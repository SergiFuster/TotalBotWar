import random
from Utilities.Vector import Vector
from Game.Action import Action


class Observation:
    def __init__(self, frame_state, team):
        """
        Creates an observation with same data that game_state
        but randomize opponent units destinations cause is a hidden info
        :param game_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        """
        if frame_state is not None:
            self.game_parameters = frame_state.game_parameters
            self.player_0_units = self.clone_list_of_units(frame_state.player_0_units)
            self.player_1_units = self.clone_list_of_units(frame_state.player_1_units)
            self.turn = team
            self.randomize_destinations(self.player_1_units if team == 0 else self.player_0_units)

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
        new_obs = Observation(self, self.turn)
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
            # new_destination = actual_direction * k (scalar), but must drop inside the screen
            max_k = self.max_k_size(unit)
            k = random.uniform(1, max_k)
            unit.set_destination(unit.position + (unit.direction * k))

    def max_k_size(self, unit):
        """
        Calculates the maximum length that the unit can move
        in the current direction without leaving the screen
        :param unit: TotalBotWar.Game.Unit.Unit
        :return: float
        """
        # Parametric equations of the straight line:
        # x = x1 + k * vx
        # y = y1 + k * vy
        x1 = unit.position.x
        y1 = unit.position.y
        vx = unit.direction.x
        vy = unit.direction.y

        if vx < 0:
            max_k_x = -(x1/vx)
        elif vx > 0:
            max_k_x = self.game_parameters.screen_size[0] / vx
        else:
            max_k_x = float("inf")

        if vy < 0:
            max_k_y = -(y1 / vy)
        elif vy > 0:
            max_k_y = self.game_parameters.screen_size[1] / vy
        else:
            max_k_y = float("inf")

        return min(max_k_x, max_k_y)

    def copy_into(self, other_observation):
        """
        Copy information from self to other_observation
        This is optimal than make a clone
        :param other_observation: TotalBotWar.Game.Observation.Observation
        :return: None
        """
        self.copy_list_of_players(self.player_0_units, other_observation.player_0_units)
        self.copy_list_of_players(self.player_1_units, other_observation.player_1_units)
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

    def get_macro_actions(self, d=20):
        """
        For every unit that can move calculate its possible actions
        moving it to 8 near portions of the unit at distance d,
        :param d: float indicating distance of the portions
        :return: List of TotalBotWar.Game.Action.Action
        """

        actions = [None]
        directions = Vector.get_basic_directions(self.turn)
        units = self.get_units(True)

        for unit in units:
            for direction in directions:
                new_pos = unit.position + (direction * d)
                if self.valid_destination(new_pos):
                    actions.append(Action(unit, new_pos.x, new_pos.y))
            actions.append(Action(unit, unit.position.x, unit.position.y))  # Stop the unit
        return actions

    def get_macro_actions_for_unit(self, unit, d=20):
        """
        Choose a random unit that can move and calculate macro actions for it
        :return: TotalBotWar.Game.Action.Action
        """

        if unit is None or not unit.available():
            return [None]   # Unit is not available

        directions = Vector.get_basic_directions(self.turn)
        actions = [None]

        for direction in directions:
            new_pos = unit.position + (direction * d)
            if self.valid_destination(new_pos):
                actions.append(Action(unit, new_pos.x, new_pos.y))
        actions.append(Action(unit, unit.position.x, unit.position.y))  # Stop the unit
        return actions

    def valid_destination(self, destination):
        """
        Indicates if destination is inside the window
        :param destination:
        :return: bool
        """
        if destination.x > self.game_parameters.screen_size[0] or destination.x < 0 or \
                destination.y > self.game_parameters.screen_size[1] or destination.y < 0:
            return False
        return True

    def get_available_random_unit(self):

        if self.turn == 0:
            units = self.clone_list_of_units(self.player_0_units)
        else:
            units = self.clone_list_of_units(self.player_1_units)

        random.shuffle(units)
        random_unit = None
        for unit in units:
            if unit.available():
                random_unit = unit
                break

        return random_unit

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

    def is_terminal(self):
        some_unit_alive = False
        for unit in self.player_0_units:
            if not unit.dead:
                some_unit_alive = True
                break
        if not some_unit_alive:
            return True

        some_unit_alive = False
        for unit in self.player_1_units:
            if not unit.dead:
                some_unit_alive = True
                break
        if not some_unit_alive:
            return True

        return self.game_parameters.remaining_time <= 0

    def get_random_action(self):
        """
        Choose a random action in available macro_actions
        :return: TotalBotWar.Game.Action.Action
        """
        actions = self.get_macro_actions()
        if len(actions) == 0:
            return None
        return random.choice(actions)
