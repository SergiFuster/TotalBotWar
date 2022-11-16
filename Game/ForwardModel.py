from typing import Union
from Utilities.Vector import Vector


class ForwardModel:

    def step(self, game_state):
        """
        Performs a game step, move or attack with each unit
        :param game_state: TotalBotWar.Game.GameState.GameState
        :return: None
        """
        units = game_state.player_0_units + game_state.player_1_units

        # If unit isn't on its destination yet
        for unit in units:
            if unit.position != unit.destination:
                self.move_unit(unit, game_state.game_parameters)

        game_state.is_terminal = self.is_terminal(game_state)

    def test(self, observation: "TotalBotWar.Game.Observation.Observation", action: "TotalBotWar.Game.Action.Action"):
        observation.is_terminal = self.is_terminal()
        pass

    def process_action(self, game_state, action):
        """
        If new destination and action is valid, set destination of unit as it's new destination
        :param game_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        :param action: TotalBotWar.Game.Observation.Observation
        :return: None
        """
        game_state.turn = (game_state.turn + 3) % 2

        unit = action.unit

        if action.destination == unit.destination:
            return

        if self.valid_destination(game_state.game_parameters.screen_size, action.destination):
            unit.set_destination(action.destination)

    def move_unit(self, unit, parameters):
        """
        Move unit towards its direction
        :param unit: TotalBotWar.Game.Unit.Unit
        :param parameters: TotalBotWar.Game.GameParameters.GameParameters
        :return: None
        """
        # If distance is lower than velocity
        if Vector.distance(unit.position, unit.destination) <= unit.velocity:
            # Set step as de vector between you and destination
            step = unit.position.direction(unit.destination)
        else:
            # Normalized direction
            direction = unit.position.direction(unit.destination).normalized()
            step = direction * unit.velocity

        # Perform movement
        unit.move(step)

        # Update unit movement parameters
        unit.move_x = not unit.position.x == unit.destination.x
        unit.move_y = not unit.position.y == unit.destination.y
        unit.moving = unit.move_x or unit.move_y

    def intersect(self, unit1, unit2):
        """
        Return a boolean indicating if unit1 and unit2 are intersecting
        :param unit1: TotalBotWar.Game.Unit.Unit
        :param unit2: TotalBotWar.Game.Unit.Unit
        :return: bool
        """
        pass

    def valid_destination(self, screen_size, destination: 'Vector') -> bool:
        """returns boolean indicating if destination is inside the window"""
        if destination.x > screen_size[0] or destination.x < 0 or \
                destination.y > screen_size[1] or destination.y < 0:
            return False
        return True

    def is_terminal(self,
                    game_state: "Union[TotalBotWar.Game.GameState.GameState,"
                                " TotalBotWar.Game.Observation.Observation]"):

        some_unit_alive = False
        for unit in game_state.player_0_units:
            if not unit.dead:
                some_unit_alive = True
        if not some_unit_alive:
            return True

        for unit in game_state.player_1_units:
            if not unit.dead:
                return False

        return True
