from Players.Player import Player


class AlwaysStoppedPlayer(Player):

    def __init__(self):
        super().__init__()

    def think(self, observation: "TotalBotWar.Game.Observation.Observation", budget: float) \
            -> "TotalBotWar.Game.Action.Action":
        """Returns an `None` to play given an `TotalBotWar.Game.Observation.Observation`.
         Performs an AFK player behaviour"""
        return None

    def __str__(self):
        return "AlwaysStoppedPlayer"
