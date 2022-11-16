import math


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

    def direction(self, other_vector: "TotalBotWar.Utilities.Vector.Vector") -> 'Vector':
        """Returns a new vector with direction from self to other"""
        if len(other_vector.value) != len(self.value):
            Exception("You can't calculate the direction between vectors of different dimensions")
        direction = []
        for i in range(0, len(other_vector.value)):
            direction.append(other_vector.value[i] - self.value[i])
        return Vector(direction)

    # region STATIC METHODS

    @staticmethod
    def distance(v1, v2):
        """Return the distance between v1 and v2"""
        return v1.direction(v2).magnitude()

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
        if abs(dot) > 1:
            Exception("Arccos of x being abs(x) > 1 is invalid")
        return math.degrees(math.acos(Vector.dot_product(v1.normalized(), v2.normalized())))

    @staticmethod
    def zero():
        """Return a Vector with axis (0, 0, 0)"""
        return Vector([0, 0, 0])

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




