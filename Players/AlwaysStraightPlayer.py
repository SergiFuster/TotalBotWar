from Players.Player import Player
from Game.Action import Action


class AlwaysStraightPlayer(Player):

    def __init__(self):
        super().__init__()

    def think(self, observation: "TotalBotWar.Game.Observation.Observation", budget: float) \
            -> "TotalBotWar.Game.Action.Action":
        """Returns an `TotalBotWar.Game.Action.Action` to play given an `TotalBotWar.Game.Observation.Observation`.
         It must return an action within the given budget of time (in seconds)."""
        units = observation.get_units()
        # print("Number of units of player 0: ", len(units))
        for unit in units:
            # print("Unit {0} of team {1} with position {2} and destination {3}".format(unit.id, unit.team, unit.position, unit.destination))
            if not unit.moving:
                # print("Destination is equal position")
                if unit.position.y == observation.game_parameters.screen_size[1]:
                    # print("Position is down border of screen")
                    return Action(unit, unit.position.x, 0)
                else:
                    # print("Position is up border of screen")
                    return Action(unit, unit.position.x, observation.game_parameters.screen_size[1])
            # print("Destination is not equal position")
        return None

    def position_unit(self, type, up_left_corner_limit, bot_right_corner_limit):
        return super().position_unit(type, up_left_corner_limit, bot_right_corner_limit)

    def __str__(self):
        return "AlwaysStraightPlayer"
