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
        random_unit = None
        for unit in units:
            if not unit.moving:
                random_unit = unit
                break

        # Not always choose a new destination
        if random_unit is not None:
            random_position = (random.randrange(1, observation.game_parameters.screen_size[0]),
                               random.randrange(1, observation.game_parameters.screen_size[1]))
            action = Action(random_unit, random_position[0], random_position[1])
        else:
            action = None

        return action

    def think_unit_position(self, type, up_left_corner_limit, bot_right_corner_limit):
        return super().think_unit_position(type, up_left_corner_limit, bot_right_corner_limit)

    def __str__(self):
        return "RandomPlayer"
