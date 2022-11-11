from Game.Direction import Direction
from typing import Union


class ForwardModel:

    def step(self, game_state: "TotalBotWar.Game.GameState.GameState", action: "TotalBotWar.Game.Action.Action"):

        units = game_state.player_0_units + game_state.player_1_units

        # If unit isn't on its destination yet
        for unit in units:
            if (unit.x, unit.y) != action.destination:
                self.move_unit(unit, game_state.game_parameters)

        game_state.is_terminal = self.is_terminal(game_state)

    def test(self, observation: "TotalBotWar.Game.Observation.Observation", action: "TotalBotWar.Game.Action.Action"):
        observation.is_terminal = self.is_terminal()
        pass

    def process_action(self,
                       game_state: Union["TotalBotWar.Game.GameState.GameState",
                                         "TotalBotWar.Game.Observation.Observation"],
                       action: "TotalBotWar.Game.Action.Action"):
        unit = action.unit

        if self.valid_destination(game_state.game_parameters.screen_size, action.destination):
            unit.set_destination(action.destination)

        game_state.turn = (game_state.turn + 3) % 2

    def move_unit(self, unit: "TotalBotWar.Game.Unit.Unit",
                  parameters: "TotalBotWar.Game.GameParameters.GameParameters"):

        pixels_x = unit.velocity if unit.destination[0] != unit.x else 0
        pixels_y = unit.velocity if unit.destination[1] != unit.y else 0

        # region MOVEMENT CORRECTION

        # region X-AXIS
        # If movement left
        if unit.direction in [Direction.SW, Direction.W, Direction.NW]:
            # if he is going to cross the line
            if (unit.x - pixels_x) < unit.destination[0]:
                pixels_x = unit.destination[0] - unit.x
            else:
                pixels_x = -pixels_x
        else:
            # if he is going to cross the line
            if (unit.x + pixels_x) > unit.destination[0]:
                pixels_x = unit.destination[0] - unit.x
        # endregion

        # region Y-AXIS
        # If movement is up
        if unit.direction in [Direction.NW, Direction.N, Direction.NE]:
            # if he is going to cross the line
            if (unit.y - pixels_y) < unit.destination[1]:
                pixels_y = unit.destination[1] - unit.y
            else:
                pixels_y = -pixels_y
        else:
            # if he is going to cross the line
            if (unit.y + pixels_y) > unit.destination[1]:
                pixels_y = unit.destination[1] - unit.y
        # endregion

        # endregion

        # Perform movement
        unit.move(pixels_x, pixels_y)

        # Update unit movement parameters
        unit.move_x = not unit.x == unit.destination[0]
        unit.move_y = not unit.y == unit.destination[1]
        unit.moving = unit.move_x or unit.move_y

    def valid_destination(self, screen_size, destination) -> bool:
        """returns boolean indicating if destination is inside the window"""
        if destination[0] > screen_size[0] or destination[0] < 0 or \
                destination[1] > screen_size[1] or destination[1] < 0:
            return False
        return True

    def is_terminal(self,
                    game_state: "Union[TotalBotWar.Game.GameState.GameState,"
                                " TotalBotWar.Game.Observation.Observation]"):

        some_unit_alive = False
        for unit in game_state.player_0_units:
            if not unit.dead:
                some_unit_alive = True
        if not some_unit_alive:
            return True

        for unit in game_state.player_1_units:
            if not unit.dead:
                return False

        return True
