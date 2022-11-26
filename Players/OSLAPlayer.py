from Players.Player import Player
from Game.Action import Action


class OSLAPlayer(Player):

    def __init__(self, heuristic):
        self.heuristic = heuristic

    def think(self, observation, budget):
        """
        Returns an `TotalBotWar.Game.Action.Action` to play given an `TotalBotWar.Game.Observation.Observation`.
         It must return an action within the given budget of time (in seconds).
        :param observation: TotalBotWar.Game.Observation.Observation
        :param budget: float
        :return: TotalBotWar.Game.Action.Action
        """
        actions = observation.get_macro_actions(2, 2)
        best_action = None
        best_reward = 0
        current_observation = observation.clone()
        for action in actions:
            if action.unit.moving:
                continue
            observation.copy_into(current_observation)
            observation.game_parameters.forward_model.simulate_seconds(current_observation, action, 1)
            reward = self.heuristic.get_reward(current_observation)
            if best_action is None or reward > best_reward:
                best_action = action
                best_reward = reward
        return best_action

    def __str__(self):
        return "OSLAPlayer"
