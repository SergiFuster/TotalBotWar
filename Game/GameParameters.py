from Game.UnitType import UnitType
from Game.Troop import Troop
from Game.ForwardModel import ForwardModel


class GameParameters:
    def __init__(self,
                 troops=None,
                 screen_size=(1000, 500),
                 screen_portions_horizontally=10,
                 screen_portions_vertically=10,
                 temp=180):
        """
        This is class-keeper to group every game modifiable parameters in one site
        :param troops: array of Troop to know which kind of troop and where position it
        :param screen_size: tuple with width and height, we need this information to can position troops accordingly
        :param screen_portions_horizontally: we use portions instead of pixels to adapt the position to every screen size
        :param screen_portions_vertically: we use portions instead of pixels to adapt the position to every screen size
        """
        if troops is None:
            troops = [Troop(UnitType.HORSE, 3, 2),
                      Troop(UnitType.SPEAR, 4, 2),
                      Troop(UnitType.SWORD, 5, 2),
                      Troop(UnitType.SWORD, 6, 2),
                      Troop(UnitType.SPEAR, 7, 2),
                      Troop(UnitType.HORSE, 8, 2),
                      Troop(UnitType.BOW, 5, 1),
                      Troop(UnitType.BOW, 6, 1),
                      Troop(UnitType.GENERAL, 5, 3)]

        self.screen_portions_horizontally = screen_portions_horizontally
        self.screen_portions_vertically = screen_portions_vertically
        self.screen_size = screen_size
        self.troops = troops
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
