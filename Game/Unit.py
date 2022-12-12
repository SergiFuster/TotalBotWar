from Utilities.Switch import Switch
from Game.UnitType import UnitType
from Utilities.Vector import Vector
import time


class Unit:
    def __init__(self, type: UnitType, id: int, x: int, y: int, team):
        """
        Construct a new Unit object
        :param type: String that determines the type of unit
        :param id: int that identifies unequivocally the unit
        :param x: int that determines x coordinate in world position of this unit
        :param y: int that determines y coordinate in world position of this unit
        :param team: int that determines the team of the unit
        :return: returns nothing
        """
        self.type = type
        self.id = id
        self.position = Vector([x, y])
        self.moving = False
        self.buffed = False
        self.team = team
        self.size = (0, 0)
        self.last_attack = time.time()                                          # Last time that attacked this unit

        self.destination = Vector([self.position.x, self.position.y])
        self.move_x = False                                                     # If it is moving in x-axis
        self.move_y = False                                                     # If it is moving in y-axis
        self.direction = Vector([0, 1]) if team == 0 else Vector([0, -1])       # In which direction is facing
        self.target = None                                                      # Unit targeted by this Unit
        self.dead = False

        # region STATS
        self.attack_rate = 1    # Attacks per second
        self.defense = 0
        self.attack = 0
        self.chargeForce = 0
        self.chargeResistance = 0
        self.velocity = 0
        self.max_health = 0
        self.health = 0
        self.farResistance = 0
        self.attackDistance = 0
        self.farAttack = 0
        self.spread_attack_radius = 0
        self.buff_radius = 0
        # Is necessary for everyone to make update_buffed_stat works correctly
        self.buff_ratio = 0
        # endregion
        self.color = []                                                         # Just for pygame visualization
        self.set_stats()

    def available(self):
        """
        Indicates if this unit can receive new destination
        :return: bool
        """
        return self.can_move()

    def can_move(self):
        """
        Return bool indicating if this unit is allowed to move
        :return: bool
        """
        return self.target is None and not self.dead

    def can_attack(self):
        """
        Indicates if self is available to performs an attack
        :return: bool
        """
        return self.target is not None and time.time() - self.last_attack >= 1 / self.attack_rate

    def can_buff(self):
        return self.type == UnitType.GENERAL

    def set_stats(self):
        """
        Give values to the Unit depending on its type
        :return: Returns nothing
        """
        with Switch(self.type) as t:
            if t.case(UnitType.SWORD):
                self.defense = 10
                self.attack = 20
                self.chargeForce = 5
                self.chargeResistance = 25
                self.velocity = 6.68
                self.size = (24.96, 12.64)
                self.health = 250
                self.max_health = self.health
                self.farResistance = 10
                self.attackDistance = 10
                self.farAttack = 0
                self.attackDistance = 10
                if self.team == 0:
                    self.color = [255, 255, 255]    # Just for pygame visualization
                else:
                    self.color = [185, 185, 185]
            if t.case(UnitType.HORSE):
                self.defense = 12
                self.attack = 12
                self.chargeForce = 100
                self.chargeResistance = 15
                self.velocity = 16.36
                self.size = (38.4, 38.4)
                self.health = 200
                self.max_health = self.health
                self.farResistance = 30
                self.attackDistance = 10
                self.farAttack = 0
                self.attackDistance = 10
                if self.team == 0:
                    self.color = [0, 0, 0]          # Just for pygame visualization
                else:
                    self.color = [70, 70, 70]
            if t.case(UnitType.SPEAR):
                self.defense = 20
                self.attack = 15
                self.chargeForce = 10
                self.chargeResistance = 125
                self.velocity = 5.6
                self.size = (48, 24)
                self.health = 250
                self.max_health = self.health
                self.farResistance = 30
                self.attackDistance = 10
                self.farAttack = 0
                self.attackDistance = 10
                if self.team == 0:
                    self.color = [255, 0, 0]        # Just for pygame visualization
                else:
                    self.color = [125, 0, 0]
            if t.case(UnitType.BOW):
                self.defense = 5
                self.attack = 10
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
                    self.color = [0, 0, 255]        # Just for pygame visualization
                else:
                    self.color = [0, 0, 125]
            if t.case(UnitType.GENERAL):
                self.defense = 10
                self.attack = 20
                self.chargeForce = 5
                self.chargeResistance = 100
                self.velocity = 6.68
                self.size = (20, 20)
                self.health = 100
                self.max_health = self.health
                self.farResistance = 10
                self.attackDistance = 100
                self.farAttack = 20
                self.spread_attack_radius = 50
                self.buff_radius = 100
                self.buff_ratio = 1.2
                if self.team == 0:
                    self.color = [255, 255, 0]        # Just for pygame visualization
                else:
                    self.color = [125, 125, 0]
            if t.default():
                raise Exception("You can't create unit {0} because {1} isn't a valid type.".format(self.id, self.type))

    def restore_stats(self):
        """
        Restore original stats for this unit, except life
        Usually used for debuff a unit
        :return: None
        """
        last_health = self.health
        self.set_stats()
        self.health = last_health
        self.buffed = False

    def try_set_target(self, unit):
        """
        Updates the appropriate attributes when a new target is assigned
        :param unit: TotalBotWar.Game.Unit.Unit - unit that must be assigned as a target
        :return: None
        """
        if self.target is None and not self.dead:
            self.set_destination(self.position)
            self.target = unit
            self.set_direction(unit.position)

    def modify_stats(self, function):
        """
        Modify the stats with function passed as argument except the life
        :param function: function
        :return: None
        """
        self.defense = function(self.defense)
        self.attack = function(self.attack)
        self.chargeForce = function(self.chargeForce)
        self.chargeResistance = function(self.chargeResistance)
        self.velocity = function(self.velocity)
        self.farResistance = function(self.farResistance)
        self.attackDistance = function(self.attackDistance)
        self.farAttack = function(self.farAttack)
        self.buffed = True

    def copy_into(self, other_unit, target=False):
        """
        Copy mutable data from self to other_unit
        this is optimal than cloning
        :param target: bool
        :param other_unit: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        self.position.copy_into(other_unit.position)
        other_unit.moving = self.moving
        other_unit.buffed = self.buffed
        other_unit.last_attack = self.last_attack
        self.destination.copy_into(other_unit.destination)
        other_unit.move_x = self.move_x
        other_unit.move_y = self.move_y
        self.direction.copy_into(other_unit.direction)
        if not target and self.target is not None:
            self.target.copy_into(other_unit.target, True)
        else:
            other_unit.target = None
        other_unit.dead = self.dead
        other_unit.health = self.health

    def take_damage(self, damage: int):
        """
        Updates self-health subtracting damage and self-dead
        :param damage: float
        :return: None
        """
        damage = 0 if damage < 0 else damage
        self.health -= damage
        if self.health <= 0:
            self.manage_death()

    def manage_death(self):
        """
        Updates all necessary attributes when the death of the unit itself occurs
        :return: None
        """
        self.set_destination(self.position)
        self.dead = True
        self.target = None

    def set_destination(self, destination):
        """
        Set new destination as destination and updates direction if new destination is not the current position
        :param destination: TotalBotWar.Utilities.Vector.Vector
        :return: None
        """
        if destination != self.position:
            self.set_direction(destination)
        self.destination = destination.clone()

    def buff_debuff(self, frame_state):
        """
        Performs an area buff for all nearby allies, himself included
        :param frame_state: Union[TotalBotWar.Game.GameState.GameState, TotalBotWar.Game.Observation.Observation]
        :return: None
        """
        if self.type != UnitType.GENERAL:
            return

        ally_units = frame_state.player_0_units if self.team == 0 else frame_state.player_1_units
        for ally in ally_units:
            if not self.dead and Vector.distance(self.position, ally.position) <= self.buff_radius:
                if not ally.buffed:
                    ally.modify_stats(lambda x: x * self.buff_ratio)
            elif ally.buffed:
                ally.restore_stats()

    def move(self, vector: Vector):
        """
        Adds vector to self-position and updates self-moving boolean
        :param vector:
        :return: None
        """
        self.position += vector
        # Update unit movement parameters
        self.move_x = self.position.x != self.destination.x
        self.move_y = self.position.y != self.destination.y
        self.moving = self.move_x or self.move_y

    def set_direction(self, position):
        """
        Assigns self-direction as the direction between self-position and position
        :param position: TotalBotWar.Utilities.Vector.Vector
        :return: None
        """
        new_direction = Vector.direction(self.position, position).normalized()
        self.direction = new_direction

    def clone(self, is_target=False):
        """
        Generate a copy of self unit
        :return: TotalBotWar.Game.Unit.Unit
        """
        new_unit = Unit(self.type, self.id, self.position.x, self.position.y, self.team)
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

    def __str__(self):
        return "I am a {0} of team {1} - {2}".format(self.id, self.team, hex(id(self)))
