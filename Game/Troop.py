class Troop:
    def __init__(self, type, x_portion, y_portion):
        """
        Construct Troop object
        :param type: The Type of Unit
        :param x_portion: x-portion of map where will be placed
        :param y_portion: y-portion of map where will be placed
        """
        self.type = type
        self.x_portion = x_portion
        self.y_portion = y_portion
