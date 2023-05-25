from Game.Units.Unit import Unit
from Utilities.Vector import Vector


class General(Unit):
    def __init__(self, id, x, y, team, screen_size):
        self.attack = 0
        self.buff_radius = 0
        self.buff_ratio = 0
        super().__init__(id, x, y, team, screen_size)

    def set_stats(self):
        self.scale = 1.97
        self.percent_width = 4.5
        self.defense = 10
        self.attack = 20
        self.chargeForce = 5
        self.chargeResistance = 100
        self.velocity = 6.68
        self.health = 100
        self.max_health = self.health
        self.farResistance = 10
        self.buff_radius = 100
        self.buff_ratio = 1.2
        if self.team == 0:
            self.color = [255, 255, 0]  # Just for pygame visualization
        else:
            self.color = [125, 125, 0]

    @property
    def type(self):
        return "g"

    def clone(self, is_target=False):
        """
        Generate a copy of self unit
        :return: TotalBotWar.Game.Unit.Unit
        """
        new_unit = General(self.id, self.position.x, self.position.y, self.team, self.screen_size)
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

    def buff_debuff(self, frame_state):
        """
        Performs an area buff for all nearby allies, himself included
        :param frame_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        :return: None
        """

        ally_units = frame_state.player_0_units if self.team == 0 else frame_state.player_1_units
        for ally in ally_units:
            if not self.dead and Vector.distance(self.position, ally.position) <= self.buff_radius:
                if not ally.buffed:
                    ally.modify_stats(lambda x: x * self.buff_ratio)
            elif ally.buffed:
                ally.restore_stats()

    def __str__(self):
        return "GENERAL"
