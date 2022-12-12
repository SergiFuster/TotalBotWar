from Players.Player import Player
from Game.Action import Action
from Utilities.Vector import Vector
import random
from Game.ForwardModel import ForwardModel


class OSLAPlayer(Player):

    def __init__(self, heuristic):
        self.heuristic = heuristic
        self.forward_model = ForwardModel()

    def think(self, observation, budget):
        """
        Returns an `TotalBotWar.Game.Action.Action` to play given an `TotalBotWar.Game.Observation.Observation`.
         It must return an action within the given budget of time (in seconds).
        :param observation: TotalBotWar.Game.Observation.Observation
        :param budget: float
        :return: TotalBotWar.Game.Action.Action
        """
        distance = 50
        actions = observation.get_macro_actions(distance)

        print("Len of actions: ", len(actions))

        current_observation = observation.clone()
        best_action = self.default_action(current_observation, distance)
        print("Start simulate frames for default action with action {0}...".format(best_action))
        self.forward_model.simulate_frames(current_observation, best_action, 5)
        print("Stop simulate frames...")
        print("Getting reward for default action...")
        best_reward = self.heuristic.get_reward(current_observation)
        print("reward for default action get")

        for action in actions:
            print("Copying observation to current observation...")
            current_observation = observation.clone()
            print("Start simulate frames for random action {0}...".format(action))
            self.forward_model.simulate_frames(current_observation, action, 5)
            print("Stop simulate frames...")
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
