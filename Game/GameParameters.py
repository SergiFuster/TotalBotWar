from Game.UnitType import UnitType
from Game.Troop import Troop


class GameParameters:
    def __init__(self, troops=None, screen_size=(1000, 500),
                 screen_portions_horizontally=10, screen_portions_vertically=10):
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
                      Troop(UnitType.BOW, 6, 1)]
        self.screen_portions_horizontally = screen_portions_horizontally
        self.screen_portions_vertically = screen_portions_vertically
        self.screen_size = screen_size
        self.troops = troops
