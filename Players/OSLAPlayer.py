from Heuristics.SimpleHeuristic import SimpleHeuristic
from Players.Player import Player
from Game.Action import Action
from Utilities.Vector import Vector
import random
from Game.ForwardModel import ForwardModel


class OSLAPlayer(Player):

    def __init__(self, heuristic=None):
        if heuristic is None:
            heuristic = SimpleHeuristic()
        self.heuristic = heuristic
        self.forward_model = ForwardModel()
        self.positions = \
            [
                [100, 100],
                [200, 100],
                [300, 100],
                [400, 100],
                [500, 100],
                [100, 200],
                [200, 200],
                [300, 200],
                [400, 200],
                [500, 200],
            ]

    def think(self, observation, budget):
        """
        Returns an `TotalBotWar.Game.Action.Action` to play given an `TotalBotWar.Game.Observation.Observation`.
         It must return an action within the given budget of time (in seconds).
        :param observation: TotalBotWar.Game.Observation.Observation
        :param budget: float
        :return: TotalBotWar.Game.Action.Action
        """
        distance = 100
        actions = observation.get_macro_actions(distance)

        current_observation = observation.clone()
        best_action = self.default_action(current_observation, distance)
        self.forward_model.simulate_frames(current_observation, best_action, 5)
        best_reward = self.heuristic.get_reward(current_observation)

        for action in actions:
            current_observation = observation.clone()
            self.forward_model.simulate_frames(current_observation, action, 5)
            reward = self.heuristic.get_reward(current_observation)
            if reward > best_reward:
                best_action = action
                best_reward = reward
        return best_action

    def default_action(self, observation, d):
        """
        Return default action, in this case go forward, for a random
        unit that is not already moving.
        :return: Action
        """
        available_units = observation.get_units(True)

        if len(available_units) > 0:
            random.shuffle(available_units)

        selected_unit = None
        for unit in available_units:
            if not unit.moving:
                selected_unit = unit
                break

        if selected_unit is None:
            return None

        target_position = selected_unit.position + (self.default_direction(selected_unit) * d)

        return Action(selected_unit, target_position.x, target_position.y)

    def position_unit(self, type, up_left_corner_limit, bot_right_corner_limit):
        return self.positions.pop()
    
    def default_direction(self, unit):
        """
        The default direction when no direction is better than other
        :param unit: TotalBotWar.Game.Unit.Unit
        :return: TotalBotWar.Utilities.Vector.Vector
        """
        if unit.team == 0:
            return Vector.south()
        else:
            return Vector.north()

    def __str__(self):
        return "OSLAPlayer"
