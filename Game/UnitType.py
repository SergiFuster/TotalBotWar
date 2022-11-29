from enum import Enum


class UnitType(Enum):
    SWORD = 0
    HORSE = 1
    SPEAR = 2
    BOW = 3
    GENERAL = 4

    def __str__(self):
        return self.name
