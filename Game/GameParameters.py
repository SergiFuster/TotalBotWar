from Game.UnitType import UnitType
from Game.Troop import Troop
from Game.ForwardModel import ForwardModel


class GameParameters:
    def __init__(self,
                 show_death_units=False,
                 show_destinations=False, show_buff_range=False,
                 show_archer_range=False, show_directions=False,
                 show_ids=False, show_health=False, show_buffed_indicator=False,
                 show_remaining_time=False, show_instructions=False,
                 show_fight_indicator=False,
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
        self.forward_model = ForwardModel()
        self.temp = temp
        self.start = 0
        self.time_elapsed = 0
        self.remaining_time = self.temp

        self.show_death_units = show_death_units
        self.show_destinations = show_destinations
        self.show_buff_range = show_buff_range
        self.show_archer_range = show_archer_range
        self.show_directions = show_directions
        self.show_ids = show_ids
        self.show_health = show_health
        self.show_buffed_indicator = show_buffed_indicator
        self.show_remaining_time = show_remaining_time
        self.show_instructions = show_instructions
        self.show_fight_indicator = show_fight_indicator

    def set_start_time(self, start):
        """
        Set start as self-start time
        :param start: float
        :return: None
        """
        self.start = start

    def update_elapsed_time(self, actual_time):
        self.time_elapsed = actual_time - self.start
        self.update_remaining_time()

    def update_remaining_time(self):
        self.remaining_time = self.temp - self.time_elapsed

    def clone(self):
        new_troops = []
        for troop in self.troops:
            new_troops.append(troop.clone())
        return GameParameters(self.show_death_units, self.show_destinations, self.show_buff_range,
                              self.show_archer_range, self.show_directions,
                              self.show_ids, self.show_health, self.show_buffed_indicator,
                              self.show_remaining_time, self.show_instructions, self.show_fight_indicator,
                              new_troops, self.screen_size[:], self.screen_portions_horizontally,
                              self.screen_portions_vertically, self.temp)
