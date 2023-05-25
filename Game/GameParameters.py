from Game.Units import *
from Game.ForwardModel import ForwardModel
from Game.Units.Unit import Unit
from Utilities.Vector import Vector
import random


class GameParameters:
    def __init__(self,
                 l_players,
                 screen_size=(1000, 500),
                 initial_positions=None,
                 central_zone_size=100,
                 temp=180):
        """
        This is class-keeper to group every game modifiable parameters in one site
        :param screen_size: tuple with width and height, we need this information to can position troops accordingly
        """
        self.central_zone_size = central_zone_size
        self.screen_size = screen_size
        self.player_0_units = []
        self.player_1_units = []
        self.forward_model = ForwardModel()
        self.temp = temp
        self.start = 0
        self.time_elapsed = 0
        self.remaining_time = self.temp

        self.show_death_units = False
        self.show_destinations = True
        self.show_buff_range = False
        self.show_archer_range = True
        self.show_directions = True
        self.show_ids = True
        self.show_health = True
        self.show_buffed_indicator = True
        self.show_remaining_time = True
        self.show_instructions = False
        self.show_fight_indicator = False
        self.setup_units(initial_positions)

    def random_initial_positions(self):
        half_down = self.screen_size[1] / 2
        initial_positions = {
            "x": random.uniform(0, self.screen_size[0]),
            "y": random.uniform(0, half_down),
            "type": "GENERAL"
        }
        for i in range(8):
            initial_positions[i] = {
                "x": random.uniform(0, self.screen_size[0]),
                "y": random.uniform(0, half_down),
                "type": self.random_type()
            }
        return initial_positions

    def random_type(self):
        types = ["ARCHER", "SWORD", "SPEAR", "KNIGHT"]
        return random.choice(types)

    def mirror_position(self, x, y):
        return (self.screen_size[0] - x), (self.screen_size[1] - y)

    def setup_units(self, initial_positions):
        if initial_positions is None:
            initial_positions = self.random_initial_positions()

        for unit in initial_positions:

            unit["type"] = unit["type"].upper()
            if unit["type"] == "ARCHER":
                mirror = self.mirror_position(unit["x"], unit["y"])

                unit_t0 = Archer.Archer(-1, unit["x"], unit["y"], 0, self.screen_size)
                unit_t1 = Archer.Archer(-1, mirror[0], mirror[1], 1, self.screen_size)

                self.player_0_units.append(unit_t0)
                self.player_1_units.append(unit_t1)

            elif unit["type"] == "SWORD":
                mirror = self.mirror_position(unit["x"], unit["y"])

                unit_t0 = Sword.Sword(-1, unit["x"], unit["y"], 0, self.screen_size)
                unit_t1 = Sword.Sword(-1, mirror[0], mirror[1], 1, self.screen_size)

                self.player_0_units.append(unit_t0)
                self.player_1_units.append(unit_t1)

            elif unit["type"] == "SPEAR":
                mirror = self.mirror_position(unit["x"], unit["y"])

                unit_t0 = Spear.Spear(-1, unit["x"], unit["y"], 0, self.screen_size)
                unit_t1 = Spear.Spear(-1, mirror[0], mirror[1], 1, self.screen_size)

                self.player_0_units.append(unit_t0)
                self.player_1_units.append(unit_t1)

            elif unit["type"] == "KNIGHT":
                mirror = self.mirror_position(unit["x"], unit["y"])

                unit_t0 = Knight.Knight(-1, unit["x"], unit["y"], 0, self.screen_size)
                unit_t1 = Knight.Knight(-1, mirror[0], mirror[1], 1, self.screen_size)

                self.player_0_units.append(unit_t0)
                self.player_1_units.append(unit_t1)

            else:
                mirror = self.mirror_position(unit["x"], unit["y"])

                unit_t0 = General.General(-1, unit["x"], unit["y"], 0, self.screen_size)
                unit_t1 = General.General(-1, mirror[0], mirror[1], 1, self.screen_size)

                self.player_0_units.append(unit_t0)
                self.player_1_units.append(unit_t1)



    def fix_initial_positions_and_destinations(self, limits):
        """
        Looks for collisions with self positioned units or
        out of limits and moves actual if is mandatory
        :param limits: tuple of list of float
        :return: None
        """
        for unit in self.player_0_units:
            if self.out_of_limits(unit.position, limits[0]):
                unit.set_position(self.random_position_inside_limits(limits[0]))
            for other in self.player_0_units:
                if unit == other:
                    continue
                while self.forward_model.intersect(unit, other):
                    direction = Vector.direction(unit.position, other.position)
                    if direction == Vector.zero():
                        direction = Vector.random()
                    other.reposition(direction.normalized())
            unit.set_destination(unit.position)

        for unit in self.player_1_units:
            if self.out_of_limits(unit.position, limits[1]):
                unit.set_position(self.random_position_inside_limits(limits[1]))
            for other in self.player_1_units:
                if unit == other:
                    continue
                while self.forward_model.intersect(unit, other):
                    direction = Vector.direction(unit.position, other.position)
                    if direction == Vector.zero():
                        direction = Vector.random()
                    other.reposition(direction.normalized())
            unit.set_destination(unit.position)


    def random_position_inside_limits(self, limit):
        return [random.randrange(limit[0][0], limit[1][0]),
                random.randrange(limit[0][1], limit[1][1])]

    def out_of_limits(self, position, limit):
        return position.x < limit[0][0] or position.x > limit[1][0] or\
               position.y < limit[0][1] or position.y > limit[1][1]

    def set_start_time(self, start):
        """
        Set start as self-start time
        :param start: float
        :return: None
        """
        self.start = start

    def update_elapsed_time(self, actual_time):
        """
        Update self-time_elapsed with time elapsed from the start of the game
        :param actual_time: time.time()
        :return: None
        """
        self.time_elapsed = actual_time - self.start
        self.update_remaining_time()

    def update_remaining_time(self):
        """
        Update self-remaining_time with the subtraction of self-temp minus self-time_elapsed
        :return: None
        """
        self.remaining_time = self.temp - self.time_elapsed


