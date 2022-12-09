from Game.Unit import Unit
import time
from Game.Observation import Observation


class GameState:
    def __init__(self, game_parameters: "TotalBotWar.Game.GameParameters.GameParameters"):
        """
        Construct GameState object
        :param game_parameters: Game.GameParameters.GameParameters that determines general information for the game
        """
        self.game_parameters = game_parameters
        self.player_0_units = []
        self.player_1_units = []
        self.turn = 0
        self.last_frame = time.time()

    def get_observation(self, team) -> "TotalBotWar.Game.Observation.Observation":
        return Observation(self, team)

    def reset(self):
        """
        This function reset values of TotalBotWar.Game.GameState.GameState parameters to its original value
        :return: return nothing
        """

        width_portion = self.game_parameters.screen_size[0] / self.game_parameters.screen_portions_horizontally
        width_portion_center = width_portion / 2

        height_portion = self.game_parameters.screen_size[1] / self.game_parameters.screen_portions_vertically
        height_portion_center = height_portion/2

        # Troops for player 0
        id = 0
        for troop in self.game_parameters.troops:
            self.player_0_units.append(Unit(troop.type, id,
                                            width_portion*troop.x_portion - width_portion_center,
                                            height_portion*troop.y_portion - height_portion_center,
                                            0))
            id += 1

        # Troops for player 1
        id = 0
        for troop in self.game_parameters.troops:
            self.player_1_units.append(Unit(troop.type, id,
                                            width_portion * troop.x_portion - width_portion_center,
                                            height_portion *
                                            (self.game_parameters.screen_portions_vertically-troop.y_portion) -
                                            height_portion_center,
                                            1))
            id += 1

        self.turn = 0

    def is_terminal(self):

        some_unit_alive = False
        for unit in self.player_0_units:
            if not unit.dead:
                some_unit_alive = True
        if not some_unit_alive:
            return True

        some_unit_alive = False
        for unit in self.player_1_units:
            if not unit.dead:
                some_unit_alive = True
        if not some_unit_alive:
            return True

        return self.game_parameters.remaining_time <= 0

    def get_winner(self):
        """
        Team with greater team health wins
        1 = win team 1
        0 = win team 0
        -1 = draw
        :return: int
        """
        health_team_0 = self.get_team_health(0)
        health_team_1 = self.get_team_health(1)
        if health_team_0 < health_team_1:
            return 1
        elif health_team_0 > health_team_1:
            return 0
        else:
            return -1

    def get_team_health(self, team):
        """
        Calculates the sum of health of the whole team
        :param team: int
        :return: int
        """
        health = 0
        if team == 0:
            for unit in self.player_0_units:
                health += unit.health if unit.health > 0 else 0
        else:
            for unit in self.player_1_units:
                health += unit.health if unit.health > 0 else 0
        return health
