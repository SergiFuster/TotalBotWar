import pygame, sys
from pygame.locals import *

BACKGROUND_GRAY = [100, 100, 100]
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]
RED = [255, 0, 0]
MAGENTA = [255, 0, 255]
BLACK = [0, 0, 0]


class GUI:
    def __init__(self, screen_size, screen_name):
        self.screen_size = screen_size
        self.screen_name = screen_name
        self.display = None
        self.screen_open = False
        self.text_size = 12
        self.font = None
        self.pause = False
        self.health_bar_width = 20
        self.health_bar_height = 3
        self.direction_line_longitude = 10

    def start_screen(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.screen_name)
        self.screen_open = True
        self.font = pygame.font.SysFont(pygame.font.get_fonts()[4], self.text_size)

    def draw_screen(self, units, debug, hud):

        """
        Initialize self.display once, manage window events and draw units, debug and hud
        :param units: List of TotalBotWar.Game.Unit.Unit
        :param debug: Bool
        :param hud: Bool
        :return: None
        """
        if not self.screen_open:
            self.start_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONUP:
                self.pause = not self.pause

        if self.pause:
            return

        self.display.fill(BACKGROUND_GRAY)
        for unit in units:

            self.draw_unit(unit)

            if debug:
                self.draw_debug(unit)
            if hud:
                self.draw_hud(unit)

        pygame.display.flip()

    def draw_unit(self, unit):
        """
        Draw a rectangle representing the unit
        :param unit: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        unit_sprite = pygame.Rect((unit.position.values[0] - unit.size[0] / 2,
                                   unit.position.values[1] - unit.size[1] / 2), unit.size)

        pygame.draw.rect(self.display, unit.color, unit_sprite)

    def draw_debug(self, unit):
        """
        Draw debug graphics
        :param unit: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        # Destination position and direction
        pygame.draw.line(self.display, GREEN, unit.position.values, unit.destination.values, 1)
        # Unit direction
        pygame.draw.line(self.display, MAGENTA, unit.position.values,
                         (unit.position + (unit.direction.normalized() * self.direction_line_longitude)).values,
                         2)

    def draw_hud(self, unit):
        """
        Draw hud graphics (life and id)
        :param unit: TotalBotWar.Game.Unit.Unit
        :return: None
        """
        # region IDs
        id = self.font.render(str(unit.id), True, WHITE)
        pos_text = unit.position.values
        pos_text[0] -= id.get_width() / 2
        pos_text[1] += unit.size[1]/2
        self.display.blit(id, pos_text)
        # endregion
        # region HEALTH
        pos_health = unit.position.values
        pos_health[1] -= unit.size[1] / 2 + self.health_bar_height + 5
        pos_health[0] -= self.health_bar_width / 2
        green_rect = pygame.Rect(pos_health[0], pos_health[1],
                                 int(unit.health / unit.max_health * self.health_bar_width), self.health_bar_height)
        red_rect = pygame.Rect(pos_health[0], pos_health[1],
                               self.health_bar_width, self.health_bar_height)
        pygame.draw.rect(self.display, RED, red_rect)
        pygame.draw.rect(self.display, GREEN, green_rect)
        # endregion
        # region Instructions
        freeze = self.font.render("C l i c k  t o  f r e e z e / u n f r e e z e  t h e  g a m e", True, BLACK)
        pos_text = [10, 0]
        self.display.blit(freeze, pos_text)

    def close_screen(self):
        pygame.quit()
        sys.exit()
