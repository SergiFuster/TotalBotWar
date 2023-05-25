from Utilities.Vector import Vector
import time


class Unit:
    def __init__(self, id, x, y, team, screen_size):
        """
        Construct a new Unit object
        :param id: int that identifies unequivocally the unit
        :param x: int that determines x coordinate in world position of this unit
        :param y: int that determines y coordinate in world position of this unit
        :param team: int that determines the team of the unit
        :return: returns nothing
        """
        # region ASSIGNABLE VARIABLES
        self.id = id
        self.position = Vector([x, y])
        self.team = team
        # endregion
        # region DEFAULT VARIABLES
        self.screen_size = screen_size
        self.selected = False
        self.moving = False
        self.buffed = False
        self.size = (0, 0)
        self.last_attack = time.time()                                          # Last time that attacked this unit
        self.destination = Vector([self.position.x, self.position.y])
        self.move_x = False                                                     # If it is moving in x-axis
        self.move_y = False                                                     # If it is moving in y-axis
        self.direction = Vector([0, 1]) if team == 0 else Vector([0, -1])       # In which direction is facing
        self.target = None                                                      # Unit targeted by this Unit
        self.dead = False
        self.archer_target = False
        # endregion
        # region COMMON STATS
        self.attack_rate = 1    # Attacks per second
        self.defense = 0
        self.chargeForce = 0
        self.chargeResistance = 0
        self.max_health = 0
        self.velocity = 0
        self.health = 0
        self.farResistance = 0
        self.color = [255, 255, 255]       # Just for pygame visualization
        self.scale = 0
        self.percent_width = 0
        # endregion
        self.set_stats()
        self.set_size()

    def set_size(self):
        width = self.percent_width * self.screen_size[0] / 100
        self.size = (width, width / self.scale)

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

    def attacking(self):
        """
        Return bool saying if unit is attacking, especially designed for database
        :return: bool
        """
        if self.target is not None: return True
        return False

    def can_buff(self):
        return str(self) == "GENERAL"

    def set_stats(self):
        """
        Give values to the Unit depending on its type
        :return: Returns nothing
        """
        pass

    @property
    def type(self):
        """
        Return string with type identifier, especially designed for database
        :return: string
        """
        pass

    @property
    def state(self):
        """
        Return string with state identifier, especially designed for database
        :return: string
        """
        if self.dead:
            return "dead"
        if self.attacking():
            return "attacking"
        if self.moving:
            return "moving"
        return "stopped"

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
            unit.archer_target = False
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
        self.chargeForce = function(self.chargeForce)
        self.chargeResistance = function(self.chargeResistance)
        self.velocity = function(self.velocity)
        self.farResistance = function(self.farResistance)
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

    def set_position(self, pos):
        """
        This is exclusive to reposition unit initially positioned out of bounds
        :param pos: list of float
        :return: None
        """
        self.position = Vector(pos)

    def move(self, vector: Vector):
        """
        Adds vector to self-position and updates self-moving boolean
        :param vector: TotalBotWar.Utilities.Vector.Vector
        :return: None
        """
        self.position += vector
        # Update unit movement parameters
        self.move_x = self.position.x != self.destination.x
        self.move_y = self.position.y != self.destination.y
        self.moving = self.move_x or self.move_y

    def reposition(self, vector):
        """
        This is similar to method move, but is just for initial repositioning,
        don't update move bool variables
        :param vector: TotalBotWar.Utilities.Vector.Vector
        :return: None
        """
        self.position += vector

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
        pass

    def update_id(self, new_id):
        self.id = new_id

    def __str__(self):
        return ""

    def serialize(self):
        """
        Convert self information to serializable format
        :param initial: Boolean
        :return: Dictionary
        """

        to_return = {"id":              self.id,
                     "state":           self.get_state(),
                     "type":            str(self),
                     "health":          round(self.health, 2),
                     "position":        self.position.serialize(),
                     "orientation":     self.direction.serialize(),
                     "width":           self.size[0],
                     "height":          self.size[1],
                     "archerTarget":   self.archer_target}
        return to_return

    def get_state(self):
        """
        Determines in which state are this unit
        :return: string
        """
        if self.dead:           return "DEAD"
        if self.attacking():    return "ATTACKING"
        if self.moving:         return "MOVING"
        return "IDLE"


