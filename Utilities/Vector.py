import math
import random


class Vector:

    def __init__(self, l_numbers):
        if len(l_numbers) < 2:
            Exception("You can't create a vector with size less than 2")
        self.value = l_numbers

    def magnitude(self) -> float:
        """Return the length of self vector"""
        squared_sum = 0
        for e in self.value:
            squared_sum += e**2

        return math.sqrt(squared_sum)

    def normalized(self) -> 'Vector':
        """Returns a new vector with same direction but length 1 or less if was smaller"""
        module = self.magnitude()

        if module <= 1:
            return self.clone()

        normalized_vector = []
        for e in self.value:
            normalized_vector.append(e/module)
        return Vector(normalized_vector)

    def clone(self):
        return Vector(self.value[:])

    def copy_into(self, other_vector):
        """
        Copy data from self to other_vector
        this is more optimal than cloning
        :param other_vector: TotalBotWar.Utilities.Vector.Vector
        :return: None
        """
        other_vector.x = self.x
        other_vector.y = self.y

    @staticmethod
    def direction(v1, v2):
        """Returns a new vector with direction from v1 to v2"""
        if len(v1) != len(v2):
            Exception("You can't calculate the direction between vectors of different dimensions")
        direction = []
        for i in range(0, len(v1)):
            direction.append(v2.value[i] - v1.value[i])
        return Vector(direction)

    # region STATIC METHODS

    @staticmethod
    def distance(v1, v2):
        """Return the distance between v1 and v2"""
        return Vector.direction(v1, v2).magnitude()

    @staticmethod
    def random():
        """
        Return a random vector
        NOT normalized
        :return: TotalBotWar.Utilities.Vector.Vector
        """
        x = random.choice([random.uniform(-1, 0), random.uniform(0.1, 1)])
        y = random.choice([random.uniform(-1, 0), random.uniform(0.1, 1)])
        return Vector([x, y])
    @staticmethod
    def dot_product(v1: 'Vector', v2: 'Vector') -> float:
        """Calculate de scalar product of 2 vectors"""
        if len(v1) != len(v2):
            Exception("Cannot calculate dot product of 2 vector with different dimensions")
        summation = 0
        for i in range(len(v1)):
            summation += v1.values[i] * v2.values[i]
        return summation

    @staticmethod
    def angle(v1: 'Vector', v2: 'Vector') -> float:
        """Return the angle between 2 vectors"""
        dot = Vector.dot_product(v1.normalized(), v2.normalized())
        dot = max(min(1.0, dot), -1.0)      # Clamping dot product [-1, 1]

        acos = math.acos(dot)
        return math.degrees(acos)


    @staticmethod
    def zero():
        """Return a Vector with axis (0, 0, 0)"""
        return Vector([0, 0, 0])

    @staticmethod
    def get_basic_directions(turn):
        """
        Return the 6 basic directions in unitary length
        :param: turn: int
        :return: List of Vectors
        """
        directions = list()
        directions.append(Vector([-1, 0]))  # west
        directions.append(Vector([1, 0]))  # east
        directions.append(Vector([0, -1]))  # north
        directions.append(Vector([0, 1]))  # south
        if turn == 1:
            directions.append(Vector([1, -1]).normalized())  # northeast
            directions.append(Vector([-1, -1]).normalized())  # northwest
        else:
            directions.append(Vector([1, 1]).normalized())  # southeast
            directions.append(Vector([-1, 1]).normalized())  # southwest

        return directions

    @staticmethod
    def south():
        return Vector([0, 1])

    @staticmethod
    def north():
        return Vector([0, -1])

    # endregion

    # region OPERATIONS

    def __eq__(self, other):
        """Compare two vectors and say if are identical, if not sort them by magnitude"""
        if not isinstance(other, Vector):
            Exception("Cannot compare Vector with non Vector")
        if self.x == other.x and self.y == other.y:
            return True
        else:
            return False

    def __mul__(self, other):
        """Return a vector with the result of multiplying its values by 'other'"""
        if not isinstance(other, int) and not isinstance(other, float):
            Exception("Cannot multiply Vector by something that's not a float or int")
        return Vector([other * value for value in self.value])

    def __add__(self, other):
        """Return the result of add other vector to self"""
        if not isinstance(other, Vector):
            Exception("Cannot add Vector by something that's not a Vector")
        return Vector([other.values[i] + self.values[i] for i in range(len(self))])

    def __sub__(self, other):
        if not isinstance(other, Vector):
            Exception("Cannot subtract Vector by something that's not a Vector")
        return Vector([self.values[i] - other.values[i] for i in range(len(other.values))])

    def __str__(self):
        return str(self.values) + "- Vector: {0} - List of Values: {1}".format(hex(id(self)), hex((id(self.value))))

    def __len__(self):
        """Return the dimension of the vector"""
        return len(self.values)

    # endregion

    # region GETTERS

    @property
    def x(self):
        return self.value[0]

    @property
    def y(self):
        return self.value[1]

    @property
    def values(self):
        """Return list with axis (copy)"""
        return self.value[:]
    # endregion

    # region SETTERS

    @x.setter
    def x(self, new_x):
        self.value[0] = new_x

    @y.setter
    def y(self, new_y):
        self.value[1] = new_y
    # endregion




