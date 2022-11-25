"""Abstract base class that defines a reward for the current `TotalBotWar.Players.Player.Player` given an
`TotalBotWar.Game.Observation.Observation`."""
from abc import ABC, abstractmethod


class Heuristic(ABC):
    """Abstract base class that defines a reward for the current `TotalBotWar.Players.Player.Player` given an
    `TotalBotWar.Game.Observation.Observation`."""

    @abstractmethod
    def get_reward(self, observation: "TotalBotWar.Game.Observation.Observation") -> float:
        """Returns a reward for the current `ASMACAG.Players.Player.Player` given an
        `TotalBotWar.Game.Observation.Observation`."""
        pass
