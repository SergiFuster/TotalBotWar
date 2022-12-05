import random
from Players.Player import Player
from Game.Action import Action


class RandomPlayer(Player):

    def __init__(self):
        super().__init__()

    def think(self, observation: "TotalBotWar.Game.Observation.Observation", budget: float) \
            -> "TotalBotWar.Game.Action.Action":
        """Returns an `TotalBotWar.Game.Action.Action` to play given an `TotalBotWar.Game.Observation.Observation`.
         It must return an action within the given budget of time (in seconds)."""
        units = observation.get_units()
        random_unit = observation.get_available_random_unit()

        # Not always choose a new destination
        if random_unit is not None:
            random_position = (random.randrange(1, observation.game_parameters.screen_size[0]),
                               random.randrange(1, observation.game_parameters.screen_size[1]))
            action = Action(random_unit, random_position[0], random_position[1])
        else:
            action = None

        return action

    def __str__(self):
        return "RandomPlayer"
