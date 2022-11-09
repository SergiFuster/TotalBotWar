from Game.Type import Type
from Game.Troop import Troop


class GameParameters:
    def __init__(self, troops=None, screen_width=1000, screen_height=500,
                 screen_portions_horizontally=10, screen_portions_vertically=10):
        """
        This is class-keeper to group every game modifiable parameters in one site
        :param troops: array of Troop to know which kind of troop and where position it
        :param screen_width: we need this information to can position troops accordingly
        :param screen_height: we need this information to can position troops accordingly
        :param screen_portions_horizontally: we use portions instead of pixels to adapt the position to every screen size
        :param screen_portions_vertically: we use portions instead of pixels to adapt the position to every screen size
        """
        if troops is None:
            troops = [Troop(Type.HORSE, 3, 2),
                      Troop(Type.SPEAR, 4, 2),
                      Troop(Type.SWORD, 5, 2),
                      Troop(Type.SWORD, 6, 2),
                      Troop(Type.SPEAR, 7, 2),
                      Troop(Type.HORSE, 8, 2),
                      Troop(Type.BOW, 5, 1),
                      Troop(Type.BOW, 6, 1)]
        self.screen_portions_horizontally = screen_portions_horizontally
        self.screen_portions_vertically = screen_portions_vertically
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.troops = troops
