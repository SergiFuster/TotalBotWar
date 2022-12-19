from Game.UnitType import UnitType
from Game.ForwardModel import ForwardModel
from Game.Unit import Unit


class GameParameters:
    def __init__(self,
                 l_players,
                 central_zone_size=100,
                 screen_size=(1000, 500),
                 temp=180):
        """
        This is class-keeper to group every game modifiable parameters in one site
        :param troops: array of Troop to know which kind of troop and where position it
        :param screen_size: tuple with width and height, we need this information to can position troops accordingly
        :param screen_portions_horizontally: we use portions instead of pixels to adapt the position to every screen size
        :param screen_portions_vertically: we use portions instead of pixels to adapt the position to every screen size
        """
        self.central_zone_size = central_zone_size
        self.screen_size = screen_size
        self.player_0_units = []
        self.player_1_units = []
        self.setup_units(l_players)
        self.temp = temp
        self.start = 0
        self.time_elapsed = 0
        self.remaining_time = self.temp

        self.show_death_units = False
        self.show_destinations = True
        self.show_buff_range = False
        self.show_archer_range = True
        self.show_directions = True
        self.show_ids = True
        self.show_health = True
        self.show_buffed_indicator = True
        self.show_remaining_time = True
        self.show_instructions = False
        self.show_fight_indicator = False

    def setup_units(self, players):

        # Troops that can place the player
        types = [UnitType.HORSE,
                 UnitType.HORSE,
                 UnitType.SWORD,
                 UnitType.SWORD,
                 UnitType.BOW,
                 UnitType.BOW,
                 UnitType.SPEAR,
                 UnitType.SPEAR,
                 UnitType.GENERAL]

        p0_up_left_corner = [0, 0]
        p0_bot_right_corner = [self.screen_size[0], self.screen_size[1]/2-self.central_zone_size/2]

        p1_up_left_corner = [0, self.screen_size[1]/2+self.central_zone_size/2]
        p1_bot_right_corner = [self.screen_size[0], self.screen_size[1]]

        print("p0 limits: [{0}, {1}] \t p1 limits: [{2}, {3}]".format(p0_up_left_corner, p0_bot_right_corner,
                                                                      p1_up_left_corner, p1_bot_right_corner))
        for type in types:
            team = 0
            for player in players:

                limits = (p0_up_left_corner, p0_bot_right_corner) if team == 0 else \
                    (p1_up_left_corner, p1_bot_right_corner)

                position = player.position_unit(type, limits[0], limits[1])
                self.fix_initial_position(position, team, limits)

                if team == 0:
                    self.player_0_units.append(Unit(type, -1, position[0], position[1], team))
                else:
                    self.player_1_units.append(Unit(type, -1, position[1], position[1], team))

                team += 1

    def fix_initial_position(self, pos, team, limits):
        """
        Looks for collisions with self positioned units or
        out of limits and moves actual if is mandatory
        :param pos: list of int
        :param team: int
        :param limits: tuple of list of float
        :return: None
        """
        troops = self.player_0_units if team == 0 else self.player_1_units
        # not implemented yet

    def set_start_time(self, start):
        """
        Set start as self-start time
        :param start: float
        :return: None
        """
        self.start = start

    def update_elapsed_time(self, actual_time):
        """
        Update self-time_elapsed with time elapsed from the start of the game
        :param actual_time: time.time()
        :return: None
        """
        self.time_elapsed = actual_time - self.start
        self.update_remaining_time()

    def update_remaining_time(self):
        """
        Update self-remaining_time with the subtraction of self-temp minus self-time_elapsed
        :return: None
        """
        self.remaining_time = self.temp - self.time_elapsed

    def clone(self):
        """
        Creates a new TotalBotWar.Game.GameParameters.GameParameters
        with the same self information cloned
        :return: TotalBotWar.Game.GameParameters.GameParameters
        """
        new_troops = []
        for troop in self.troops:
            new_troops.append(troop.clone())
        return GameParameters(new_troops, self.screen_size[:], self.screen_portions_horizontally,
                              self.screen_portions_vertically, self.temp)
