from Game.Unit import Unit
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
        self.is_terminal = False
        self.turn = 0

    def get_observation(self) -> "TotalBotWar.Game.Observation.Observation":
        return Observation(self)

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
