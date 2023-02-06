from Game.Units.Unit import Unit


class Archer(Unit):
    def __init__(self, id, x, y, team):
        self.attackDistance = 0
        self.farAttack = 0
        self.spread_attack_radius = 0
        super().__init__(id, x, y, team)

    def set_stats(self):
        self.defense = 5
        self.chargeForce = 5
        self.chargeResistance = 0
        self.velocity = 6.68
        self.size = (52, 20.8)
        self.health = 100
        self.max_health = self.health
        self.farResistance = 10
        self.attackDistance = 100
        self.farAttack = 20
        self.spread_attack_radius = 50
        if self.team == 0:
            self.color = [0, 0, 255]  # Just for pygame visualization
        else:
            self.color = [0, 0, 125]

    @property
    def type(self):
        return "a"

    def clone(self, is_target=False):
        """
        Generate a copy of self unit
        :return: TotalBotWar.Game.Unit.Unit
        """
        new_unit = Archer(self.id, self.position.x, self.position.y, self.team)
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
        self.attackDistance = function(self.attackDistance)
        self.farAttack = function(self.farAttack)

    def __str__(self):
        return "ARCHER"
