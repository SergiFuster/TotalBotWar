from Game.Units.Unit import Unit


class Knight(Unit):
    def __init__(self, id, x, y, team, screen_size):
        self.attack = 0
        super().__init__(id, x, y, team, screen_size)

    def set_stats(self):
        self.scale = 1
        self.percent_width = 8.84
        self.defense = 12
        self.attack = 12
        self.chargeForce = 100
        self.chargeResistance = 15
        self.velocity = 16.36
        self.health = 200
        self.max_health = self.health
        self.farResistance = 30
        if self.team == 0:
            self.color = [0, 0, 0]  # Just for pygame visualization
        else:
            self.color = [70, 70, 70]

    @property
    def type(self):
        return "k"

    def clone(self, is_target=False):
        """
        Generate a copy of self unit
        :return: TotalBotWar.Game.Unit.Unit
        """
        new_unit = Knight(self.id, self.position.x, self.position.y, self.team, self.screen_size)
        new_unit.destination = self.destination.clone()
        new_unit.direction = self.direction.clone()
        new_unit.health = self.health
        new_unit.moving = self.moving
        new_unit.buffed = self.buffed
        new_unit.move_x = self.move_x
        new_unit.move_y = self.move_y
        new_unit.target = self.target.clone(True) if self.target is not None and not is_target else None
        new_unit.dead = self.dead

        return new_unit

    def modify_stats(self, function):
        """
        Modify the stats with function passed as argument except the life
        :param function: function
        :return: None
        """
        super().modify_stats(function)
        self.attack = function(self.attack)

    def __str__(self):
        return "KNIGHT"
