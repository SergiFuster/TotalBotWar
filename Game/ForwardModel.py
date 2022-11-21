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

        # Charge execution and fighting state updater
        for unit_p0 in game_state.player_0_units:
            for unit_p1 in game_state.player_1_units:

                # Unit doesn't update target until finishing with actual one
                if unit_p0.target is not None and unit_p1.target is not None:
                    continue

                if self.intersect(unit_p0, unit_p1):
                    print("Unit {0} of team 0 intersected with unit {1} of team 1".format(unit_p0.id, unit_p1.id))
                    self.manage_intersection(unit_p0, unit_p1)
                    print()

        # If unit isn't on its destination yet
        for unit in units:
            if unit.moving and unit.target is None:
                self.move_unit(unit, game_state.game_parameters)

        game_state.is_terminal = self.is_terminal(game_state)

    def manage_intersection(self, unit0, unit1):
        """
        Execute charge and update target if necessary
        :param unit0: Main Unit
        :param unit1: Unit target
        :return: None
        """
        if unit0.target is None:
            direction_to_target = Vector.direction(unit0.position, unit1.position)
            angle_to_target = Vector.angle(unit0.direction, direction_to_target)
            print("Angle between direction of unit {0} of team 0 and unit {1} of team 1: {2}".format(unit0.id, unit1.id,
                                                                                                     angle_to_target))
            # If it is moving and its target is in front of him
            if unit0.moving and angle_to_target < 90:
                self.charge(unit0, unit1)
            unit0.set_destination(unit0.position)
            unit0.target = unit1.id

        if unit1.target is None:
            direction_to_target = Vector.direction(unit1.position, unit0.position)
            angle_to_target = Vector.angle(unit1.direction, direction_to_target)
            print("Angle between direction of unit {0} of team 1 and unit {1} of team 0: {2}".format(unit1.id, unit0.id,
                                                                                                     angle_to_target))
            # If it is moving and its target is in front of him
            if unit1.moving and angle_to_target < 90:
                self.charge(unit1, unit0)
            unit1.set_destination(unit1.position)
            unit1.target = unit0.id

    def charge(self, unit0, unit1):
        """
        Charge from unit0 to unit1
        :param unit0: Main Unit
        :param unit1: Target Unit
        :return: None
        """
        direction_of_impact = Vector.direction(unit1.position, unit0.position)
        angle_of_impact = Vector.angle(unit1.direction, direction_of_impact)
        impact_force = 1 if angle_of_impact < 90 else 3
        damage = unit0.chargeForce - (unit1.chargeResistance / impact_force)

        # Avoiding add life if unit1 have much chargeResistance
        damage = damage if damage > 0 else 0

        unit1.take_damage(damage)

    def test(self, observation: "TotalBotWar.Game.Observation.Observation", action: "TotalBotWar.Game.Action.Action"):
        observation.is_terminal = self.is_terminal()
        pass

    def process_action(self, game_state, action):
        """
        If new destination and action is valid, set destination of unit as its new destination
        :param game_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        :param action: TotalBotWar.Game.Observation.Observation
        :return: None
        """
        game_state.turn = (game_state.turn + 3) % 2

        if action is None:
            return

        # (game_state.turn + 3) % 2 it's the opposite turn of game_state.turn
        unit = self.get_unit_by_id_and_turn(game_state, action.unit.id, (game_state.turn + 3) % 2)

        # This statement is temporal, cause move unit that is fighting is still allowed
        if unit.target is not None:
            return

        if self.valid_destination(game_state.game_parameters.screen_size, action.destination):
            unit.set_destination(action.destination)

    def get_unit_by_id_and_turn(self, game_state, id, turn):
        """
        Return the unit with unit.id == id and unit.team == turn
        :param game_state: TotalBotWar.Game.GameState.GameState
        :param id: int
        :param turn: int
        :return: TotalBotWar.Game.Unit.Unit
        """
        if id < 0 or \
                id >= len(game_state.player_0_units) and turn == 0 or \
                id >= len(game_state.player_1_units) and turn == 1:
            Exception("Unit with id {0} doesn't exist".format(id))

        if turn == 0:
            return game_state.player_0_units[id]
        else:
            return game_state.player_1_units[id]

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
            step = Vector.direction(unit.position, unit.destination)
        else:
            # Normalized direction
            direction = Vector.direction(unit.position, unit.destination)
            direction = direction.normalized()
            step = direction * unit.velocity

        # Perform movement
        unit.move(step)

        # Update unit movement parameters
        unit.move_x = unit.position.x != unit.destination.x
        unit.move_y = unit.position.y != unit.destination.y
        unit.moving = unit.move_x or unit.move_y

    def intersect(self, unit0, unit1):
        """
        Return a boolean indicating if unit0 and unit1 are intersecting
        :param unit0: TotalBotWar.Game.Unit.Unit
        :param unit1: TotalBotWar.Game.Unit.Unit
        :return: bool
        """
        return self.collide_in_x_axis(unit0, unit1) and self.collide_in_y_axis(unit0, unit1)

    def collide_in_x_axis(self, unit0, unit1):
        return (unit0.position.x + unit0.size[0] / 2) > unit1.position.x - unit1.size[0] / 2 and \
                unit0.position.x + unit0.size[0] / 2 < unit1.position.x + unit1.size[0] / 2 + unit0.size[0]

    def collide_in_y_axis(self, unit0, unit1):
        return (unit0.position.y + unit0.size[1] / 2) > unit1.position.y - unit1.size[1] / 2 and \
                unit0.position.y + unit0.size[1] / 2 < unit1.position.y + unit1.size[1] / 2 + unit0.size[1]

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
