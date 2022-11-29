from typing import Union
from Utilities.Vector import Vector
import time
import random


class ForwardModel:

    def step(self, frame_state):
        """
        Performs a game step, move or attack with each unit
        :param frame_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        :return: None
        """
        units = frame_state.player_0_units + frame_state.player_1_units
        random.shuffle(units)
        # Charge execution and fighting state updater for every combination of 2 units between teams
        for unit_p0 in frame_state.player_0_units:
            for unit_p1 in frame_state.player_1_units:

                if unit_p0.dead or unit_p1.dead:
                    continue

                # Check if archer its close enough to set its target
                if str(unit_p0.type) == "BOW":
                    self.check_archer(unit_p0, unit_p1)

                if str(unit_p1.type) == "BOW":
                    self.check_archer(unit_p1, unit_p0)

                # Unit doesn't update target until finishing with actual one
                if not unit_p0.moving and not unit_p1.moving:
                    continue

                if self.intersect(unit_p0, unit_p1):
                    self.manage_intersection(unit_p0, unit_p1)

        # Fight or movement execution for every unit
        for unit in units:

            if unit.dead:
                continue

            unit.update_buffed_state()      # Undoes the effect of the buff it had if the time of the buff has expired

            # General buff nearby allys every time that he can
            if unit.can_buff():
                unit.buff(frame_state)

            # Basic actions, move and attack
            if unit.can_move():
                self.move_unit(unit, frame_state.game_parameters)
            elif unit.can_attack():
                if str(unit.type) == "BOW":
                    self.archer_attack(unit, frame_state)
                else:
                    self.attack(unit)

    def check_archer(self, archer, target):
        """
        Checks if target is on range and updates it if so
        :param archer: TotalBotWar.Game.Unit.Unit
        :param target: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        distance = Vector.distance(archer.position, target.position)
        if distance <= archer.attackDistance:
            archer.try_set_target(target)

    def archer_attack(self, archer, frame_state):
        """
        Executes attack from archer to its target and all around it
        :param frame_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        :param archer: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        if archer.target.dead or Vector.distance(archer.position, archer.target.position) > archer.attackDistance:
            archer.target = None
        else:
            archer.set_direction(archer.target.position)
            enemy_units = frame_state.player_0_units if archer.team == 1 else frame_state.player_1_units
            for unit in enemy_units:
                distance = Vector.distance(unit.position, archer.target.position)
                if distance <= archer.spread_attack_radius:
                    attack_bonus = 2 if self.bonus_by_type(archer.type, unit.type) else 1
                    damage = archer.farAttack * attack_bonus - unit.farResistance / 2
                    unit.take_damage(damage)
            archer.last_attack = time.time()

    def attack(self, unit):
        """
        Executes attack from unit to unit-target
        :param unit: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        if unit.target.dead:
            unit.target = None
        else:
            attack_bonus = 2 if self.bonus_by_type(unit.type, unit.target.type) else 1
            unit.last_attack = time.time()
            damage = unit.attack * attack_bonus - unit.target.defense / 2
            unit.target.take_damage(damage)

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
            # If it is moving and its target is in front of him
            if unit0.moving and angle_to_target < 90:
                self.charge(unit0, unit1)

        if unit1.target is None:
            direction_to_target = Vector.direction(unit1.position, unit0.position)
            angle_to_target = Vector.angle(unit1.direction, direction_to_target)
            # If it is moving and its target is in front of him
            if unit1.moving and angle_to_target < 90:
                self.charge(unit1, unit0)

        # Update the stats at the end so as not to affect the unit1 direction prior its charge
        unit0.try_set_target(unit1)
        unit1.try_set_target(unit0)

    def charge(self, unit0, unit1):
        """
        Charge from unit0 to unit1
        :param unit0: Main Unit
        :param unit1: Target Unit
        :return: None
        """
        direction_of_impact = Vector.direction(unit1.position, unit0.position)
        angle_of_impact = Vector.angle(unit1.direction, direction_of_impact)
        # If impact is from behind or sides, resistance is reduced
        resistance_reduction = 1 if angle_of_impact < 90 else 3

        impact_bonus = 10 if self.bonus_by_type(unit0.type, unit1.type) else 1

        print("Charger type: {0} \nReceiver type: {1} \nAngle of impact: {2}".format(unit0.type, unit1.type,
                                                                                     angle_of_impact))
        print("Charger force: {0} \nReceiver resistance: {1} \nImpact bonus: {2} \n"
              "Resistance reduction: {3} \nEquation: {0} * {2} - {1} / {3}".format(unit0.chargeForce,
                                                                                   unit1.chargeResistance,
                                                                                   impact_bonus,
                                                                                   resistance_reduction))
        print()

        damage = (unit0.chargeForce * impact_bonus) - (unit1.chargeResistance / resistance_reduction)

        # Avoiding add life if unit1 have much chargeResistance
        damage = damage if damage > 0 else 0

        unit1.take_damage(damage)

    def bonus_by_type(self, type_charger, type_receiver):
        """
        Get a number that indicates if charger have type bonus over receiver
        :param type_charger: TotalBotWar.Game.UnitType.UnitType
        :param type_receiver: TotalBotWar.Game.UnitType.UnitType
        :return: int
        """

        if str(type_charger) == "SWORD" and str(type_receiver) == "SPEAR" or \
                str(type_charger) == "SPEAR" and str(type_receiver) == "HORSE" or \
                str(type_charger) == "HORSE" and str(type_receiver) == "SWORD" or \
                str(type_receiver) == "BOW":

            return True

        else:
            return False

    def simulate_seconds(self, observation: "TotalBotWar.Game.Observation.Observation",
                         action: "TotalBotWar.Game.Action.Action", seconds=1):
        """
        Play an action and simulate game for seconds as if no one was playing any further action
        Modify the observation passed as an argument
        :param observation: TotalBotWar.Game.Observation.Observation
        :param action: TotalBotWar.Game.Action.Action
        :param seconds: int
        :return: None
        """
        self.process_action(observation, action)
        iterations = observation.game_parameters.frame_rate * seconds
        while not observation.is_terminal() and iterations > 0:
            self.step(observation)
            iterations -= 1

    def simulate_frames(self, observation: "TotalBotWar.Game.Observation.Observation",
                        action: "TotalBotWar.Game.Action.Action", frames=1):
        """
        Play an action and simulate game for frames as if no one was playing any further action
        Modify the observation passed as an argument
        :param observation: TotalBotWar.Game.Observation.Observation
        :param action: TotalBotWar.Game.Action.Action
        :param frames: int
        :return: None
        """
        self.process_action(observation, action)
        while not observation.is_terminal and frames > 0:
            self.step(observation)
            frames -= 1

    def process_action(self, frame_state, action):
        """
        If new destination and action is valid, set destination of unit as its new destination
        :param frame_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        :param action: TotalBotWar.Game.Observation.Observation
        :return: None
        """
        frame_state.turn = (frame_state.turn + 3) % 2

        if action is None:
            return

        # (game_state.turn + 3) % 2 it's the opposite turn of game_state.turn
        unit = self.get_unit_by_id_and_turn(frame_state, action.unit.id, (frame_state.turn + 3) % 2)

        # This statement is temporal, cause move unit that is fighting is still allowed
        if unit.target is not None:
            return

        if self.valid_destination(frame_state.game_parameters.screen_size, action.destination):
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
