import pygame
import sys
from pygame.locals import *

BACKGROUND_GRAY = [100, 100, 100]
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
MAGENTA = [255, 0, 255]
BLACK = [0, 0, 0]
YELLOW = [255, 255, 0]
ORANGE = [255, 165, 0]


class GUI:
    def __init__(self, game_parameters, screen_name, ):
        self.game_parameters = game_parameters
        self.screen_name = screen_name
        self.display = None
        self.screen_open = False
        self.text_size = 20
        self.font = None
        self.pause = False
        self.health_bar_width = 20
        self.health_bar_height = 3
        self.direction_line_longitude = 10
        self.swords = pygame.image.load("Images/crossed_swords.png")
        self.swords = pygame.transform.scale(self.swords, (50, 50))

    def start_screen(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.game_parameters.screen_size)
        pygame.display.set_caption(self.screen_name)
        self.screen_open = True
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[4], self.text_size)

    def draw_final_screen(self, message):
        for event in pygame.event.get():
            if event.type == QUIT:
                self.close_screen()
            if event.type == pygame.MOUSEBUTTONUP:
                pass
        self.display.fill(BACKGROUND_GRAY)
        final_message = self.font.render(message, True, WHITE)
        pos_text = (self.game_parameters.screen_size[0]/2-final_message.get_width()/2,
                    self.game_parameters.screen_size[1]/2-final_message.get_height())
        self.display.blit(final_message, pos_text)
        pygame.display.flip()

    def draw_screen(self, units, remaining_time):

        """
        Initialize self-display once, manage window events and draw units, debug and hud
        :param units: List of TotalBotWar.Game.Unit.Unit
        :param remaining_time: float with time left
        :return: bool that indicates if game is paused
        """
        click = None
        if not self.screen_open:
            self.start_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                self.close_screen()
            if event.type == pygame.MOUSEBUTTONUP:
                click = pygame.mouse.get_pos()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.pause = not self.pause

        if self.pause:
            return self.pause

        self.display.fill(BACKGROUND_GRAY)

        self.draw_hud(remaining_time)

        for unit in units:
            if not unit.dead or self.game_parameters.show_death_units:
                self.draw_unit(unit)

        pygame.display.flip()

        return self.pause, click

    def draw_unit(self, unit):
        """
        Draw a rectangle representing the unit
        :param unit: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        unit_sprite = pygame.Rect((unit.position.values[0] - unit.size[0] / 2,
                                   unit.position.values[1] - unit.size[1] / 2), unit.size)

        pygame.draw.rect(self.display, unit.color, unit_sprite)

        # region DEBUG AND HUD
        # region ID
        if self.game_parameters.show_ids:
            id = self.font.render(str(unit.id), True, WHITE)
            pos_text = unit.position.values
            pos_text[0] -= id.get_width() / 2
            pos_text[1] += unit.size[1] / 2
            self.display.blit(id, pos_text)
        # endregion
        # region HEALTH
        if self.game_parameters.show_health:
            health = self.font.render("{0:.1f}".format(unit.health), True, GREEN)
            pos_health = unit.position.values
            pos_health[0] -= health.get_width() / 2
            pos_health[1] -= unit.size[1] / 2 + health.get_height()
            self.display.blit(health, pos_health)
            # region HEALTHBAR
            # pos_health[1] -= unit.size[1] / 2 + self.health_bar_height + 5
            # pos_health[0] -= self.health_bar_width / 2
            # green_rect = pygame.Rect(pos_health[0], pos_health[1],
            #                          int(unit.health / unit.max_health * self.health_bar_width),
            #                          self.health_bar_height)
            # red_rect = pygame.Rect(pos_health[0], pos_health[1],
            #                        self.health_bar_width, self.health_bar_height)
            # pygame.draw.rect(self.display, RED, red_rect)
            # pygame.draw.rect(self.display, GREEN, green_rect)
            # endregion
        # endregion
        # region RANGE
        if self.game_parameters.show_archer_range and str(unit) == "ARCHER":
            pygame.draw.circle(self.display, RED, unit.position.values, unit.attackDistance, 1)
            if unit.target is not None:
                pygame.draw.circle(self.display, YELLOW, unit.target.position.values, unit.spread_attack_radius, 1)
        # endregion
        # region BUFF
        if self.game_parameters.show_buff_range and str(unit) == "GENERAL":
            pygame.draw.circle(self.display, ORANGE, unit.position.values, unit.buff_radius, 1)
        if self.game_parameters.show_buffed_indicator:
            if unit.buffed:
                points = [(unit.position.x - unit.size[0] / 2, unit.position.y - unit.size[1] / 2 - 2),
                          (unit.position.x - unit.size[0] / 2 + 2, unit.position.y - unit.size[1] / 2 - 4),
                          (unit.position.x - unit.size[0] / 2 + 4, unit.position.y - unit.size[1] / 2 - 2)]
                pygame.draw.polygon(self.display, YELLOW, points)
        # endregion
        # region DESTINATION
        if self.game_parameters.show_destinations:
            # Destination position
            pygame.draw.line(self.display, GREEN, unit.position.values, unit.destination.values, 1)
        # endregion
        # region FIGHT
        if self.game_parameters.show_fight_indicator and unit.target is not None:
            swords_pos = unit.position.values
            swords_pos[0] -= self.swords.get_width() / 2
            swords_pos[1] -= self.swords.get_height() / 2
            self.display.blit(self.swords, swords_pos)
        # endregion
        # region DIRECTION
        if self.game_parameters.show_directions:
            # Unit direction
            pygame.draw.line(self.display, MAGENTA, unit.position.values,
                             (unit.position + (unit.direction.normalized() * self.direction_line_longitude)).values,
                             2)
        # endregion
        # endregion

    def draw_hud(self, remaining_time):
        """
        Draw hud graphics (time and options)
        :param remaining_time: float
        :return: None
        """
        # region TIME
        if self.game_parameters.show_remaining_time:
            time = self.font.render("{0:.0f}".format(remaining_time), True, BLACK)
            pos_text = [self.game_parameters.screen_size[0] - time.get_width() - 10, 10]
            self.display.blit(time, pos_text)
        # endregion
        # region Instructions
        if self.game_parameters.show_instructions:
            freeze = self.font.render("S p a c e  t o  f r e e z e / u n f r e e z e  t h e  g a m e", True, BLACK)
            pos_text = [10, 10]
            self.display.blit(freeze, pos_text)
        # endregion

    def close_screen(self):
        self.screen_open = False
        pygame.quit()
        sys.exit()
