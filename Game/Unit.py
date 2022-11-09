from Utilities.Switch import Switch
from Game.Type import Type


class Unit:
    def __init__(self, type: Type, id: int, x: int, y: int):
        """
        Construct a new Unit object
        :param type: String that determines the type of unit
        :param id: int that identifies unequivocally the unit
        :param x: int that determines x coordinate in world position of this unit
        :param y: int that determines y coordinate in world position of this unit
        :return: returns nothing
        """
        self.type = type
        self.id = id
        self.x = x
        self.y = y
        self.moving = False
        self.buffed = False

        self.next_x = self.y    # Where is going the unit in x-axis
        self.next_y = self.x    # Where is going the unit in y-axis
        self.move_x = False     # If it is moving in x-axis
        self.move_y = False     # If it is moving in y-axis
        self.direction = None   # In which direction is facing
        self.target = None      # Unit targeted by this Unit
        self.dead = False

        # region STATS
        self.defense = 0
        self.attack = 0
        self.chargeForce = 0
        self.chargeResistance = 0
        self.velocity = 0
        self.life = 0
        self.farResistance = 0
        self.attackDistance = 0
        self.farAttack = 0
        # endregion
        self.set_stats()

        self.color = []         # Just for pygame visualization

    def set_stats(self):
        """
        Give values to the Unit depending on its type
        :return: Returns nothing
        """
        with Switch(self.type) as t:
            if t.case(Type.SWORD):
                self.defense = 10
                self.attack = 20
                self.chargeForce = 5
                self.chargeResistance = 25
                self.velocity = 15
                self.life = 250
                self.farResistance = 10
                self.attackDistance = 10
                self.farAttack = 0
                self.color = [255, 255, 255]    # Just for pygame visualization
            if t.case(Type.HORSE):
                self.defense = 12
                self.attack = 12
                self.chargeForce = 100
                self.chargeResistance = 15
                self.velocity = 40
                self.life = 200
                self.farResistance = 30
                self.attackDistance = 10
                self.farAttack = 0
                self.color = [0, 0, 0]          # Just for pygame visualization
            if t.case(Type.SPEAR):
                self.defense = 20
                self.attack = 15
                self.chargeForce = 10
                self.chargeResistance = 125
                self.velocity = 10
                self.life = 250
                self.farResistance = 30
                self.attackDistance = 10
                self.farAttack = 0
                self.color = [255, 0, 0]        # Just for pygame visualization
            if t.case(Type.BOW):
                self.defense = 5
                self.attack = 10
                self.chargeForce = 5
                self.chargeResistance = 0
                self.velocity = 15
                self.life = 100
                self.farResistance = 10
                self.attackDistance = 450
                self.farAttack = 20
                self.color = [0, 0, 255]        # Just for pygame visualization
            if t.default():
                raise Exception("You can't create unit {0} because {1} isn't a valid type.".format(self.id, self.type))

    def restore_stats(self):
        last_life = self.life
        self.set_stats()
        self.life = last_life

    def modify_stats(self, function):
        """
        Modify the stats with function passed as argument except the life
        :param function: function
        :return: return nothing
        """
        self.defense = function(self.defense)
        self.attack = function(self.attack)
        self.chargeForce = function(self.chargeForce)
        self.chargeResistance = function(self.chargeResistance)
        self.velocity = function(self.velocity)
        self.farResistance = function(self.farResistance)
        self.attackDistance = function(self.attackDistance)
        self.farAttack = function(self.farAttack)

    def take_damage(self, damage: int):
        self.life -= damage
        self.dead = self.life <= 0

    def __str__(self):
        return ("I am a {0} with ID {1} and stats: \n"
                "{2} defense,\n"
                "{3} attack,\n"
                "{4} charge force,\n"
                "{5} charge resistance,\n"
                "{6} velocity,\n"
                "{7} life,\n"
                "{8} far resistance,\n"
                "{9} attack distance,\n"
                "{10} far attack,"
                "{11} color.\n"
                "And my position is x: {12} and y: {13} ".format(self.type.name, self.id, self.defense, self.attack,
                                                                 self.chargeForce, self.chargeResistance, self.velocity,
                                                                 self.life, self.farResistance, self.attackDistance,
                                                                 self.farAttack, self.color, self.x, self.y))
