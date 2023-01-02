from Players.Player import Player
from Game.ForwardModel import ForwardModel


class HumanPlayer(Player):

    def __init__(self):
        super().__init__()
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
        return None

    def position_unit(self, type, up_left_corner_limit, bot_right_corner_limit):
        return self.positions.pop()

    def __str__(self):
        return "HumanPlayer"
