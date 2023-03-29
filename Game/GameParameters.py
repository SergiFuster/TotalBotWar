from Game.Units import *
from Game.ForwardModel import ForwardModel
from Game.Units.Unit import Unit
from Utilities.Vector import Vector
import random


class GameParameters:
    def __init__(self,
                 l_players,
                 central_zone_size=100,
                 screen_size=(1000, 500),
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
        self.setup_units(l_players)
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

    def setup_units(self, players):

        # Troops that can place the player
        # region instructions
        # K = Knight
        # S = Sword
        # P = Spear
        # A = Archer
        # G = General
        # endregion
        types ="KKSSPPAAG"
        p0_up_left_corner = [0, 0]
        p0_bot_right_corner = [self.screen_size[0], self.screen_size[1]/2-self.central_zone_size/2]

        p1_up_left_corner = [0, self.screen_size[1]/2+self.central_zone_size/2]
        p1_bot_right_corner = [self.screen_size[0], self.screen_size[1]]

        limits = ((p0_up_left_corner, p0_bot_right_corner), (p1_up_left_corner, p1_bot_right_corner))

        for letter in types:
            team = 0
            for player in players:

                limit = limits[team]

                position = player.position_unit(type, limit[0], limit[1])

                if letter == "K":
                    unit = Knight.Knight(-1, position[0], position[1], team)
                elif letter == "S":
                    unit = Sword.Sword(-1, position[0], position[1], team)
                elif letter == "P":
                    unit = Spear.Spear(-1, position[0], position[1], team)
                elif letter == "G":
                    unit = General.General(-1, position[0], position[1], team)
                else:
                    unit = Archer.Archer(-1, position[0], position[1], team)

                if team == 0:
                    self.player_0_units.append(unit)
                else:
                    self.player_1_units.append(unit)

                team += 1

        self.fix_initial_positions(limits)

    def fix_initial_positions(self, limits):
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


