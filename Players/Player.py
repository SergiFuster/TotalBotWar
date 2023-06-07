import random
import time
from abc import ABC, abstractmethod


class Player(ABC):
    """Abstract base class for an entity with a defined behaviour for playing a `TotalBotWar.Game.Game.Game`."""
    def __init__(self, heuristic=None):
        self.heuristic = heuristic

    @abstractmethod
    def think(self, observation, budget):
        """Returns an `TotalBotWar.Game.Action.Action` to play given an `TotalBotWar.Game.Observation.Observation`. It must
        return an action within the given budget of time (in seconds)."""

    @abstractmethod
    def __str__(self):
        return "Player"
