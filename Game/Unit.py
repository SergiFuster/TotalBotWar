import Type
from Utilities import Switch

class Unit:
    def __init__(self, type, id, x, y):
        """
        Construct a new Unit object
        :param type: String that determines the type of unit
        :param id: int that identifies unequivocally the unit
        :param x: int that determines x coordinate in world position of this unit
        :param y: int that determines y coordinate in world position of this unit
        :attribute direction: Direction that determine the direction Unit is facing
        :return: returns nothing
        """
        self.type = Type.Type[type]
        self.id = id
        self.x = x
        self.y = y
        self.direction = None
        self.moving = False
        self.setStats()

    def setStats(self):
        """
        Give values to the Unit depending on its type
        :return: Returns nothing
        """
        switch = Switch()
        with switch(self.type) as t:
            if t.case(Type.SOWRD):
                self.defense = 10
                self.attack = 20
                self.chargeForce = 5
                self.chargeResistance = 25
                self.velocity = 15
                self.life = 250
                self.farResistance = 10
            if t.case(Type.SPEAR):
                self.defense = 10
                self.attack = 20
                self.chargeForce = 5
                self.chargeResistance = 25
                self.velocity = 15
                self.life = 250
                self.farResistance = 10
            if t.case(Type.HORSE):
                self.defense = 10
                self.attack = 20
                self.chargeForce = 5
                self.chargeResistance = 25
                self.velocity = 15
                self.life = 250
                self.farResistance = 10
            if t.case(Type.BOW):
                self.defense = 10
                self.attack = 20
                self.chargeForce = 5
                self.chargeResistance = 25
                self.velocity = 15
                self.life = 250
                self.farResistance = 10
            if t.default():
                """
                TODO
                throw some exception cause that type doesn't exist
                """

