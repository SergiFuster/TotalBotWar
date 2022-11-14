from Utilities.Vector import Vector


class Action:
    def __init__(self, unit: "TotalBotWar.Game.Unit.Unit", x: int, y: int):
        """
        Construct a new Action object
        :param unit: Unit that performs the action
        :param x: x-axis where is going the Unit
        :param y: y-axis where is going the Unit
        """
        self.unit = unit
        self.destination = Vector([x, y])

    def __str__(self):
        return "{0} {1} {2}".format(self.unit.id, self.destination.x, self.destination.y)

    def __eq__(self, other):
        """
        When Action is compared with other object
        with == returns according to this function
        :param other: whatever object
        :return: returns boolean indicating if both have the same id
        """
        if isinstance(other, Action):
            return self.unit.id == other.unit.id
        else:
            return False
