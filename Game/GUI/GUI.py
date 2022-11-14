import pygame, sys
from pygame.locals import *

BACKGROUND_GRAY = [100, 100, 100]
GREEN = [0, 255, 0]
WHITE = [255, 255, 255]

class GUI:
    def __init__(self, screen_size, screen_name):
        self.screen_size = screen_size
        self.screen_name = screen_name
        self.display = None
        self.screen_open = False
        self.text_size = 12
        self.font = None
        self.health_bar_width = 20
        self.health_bar_height = 3

    def start_screen(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.screen_name)
        self.screen_open = True
        self.font = pygame.font.SysFont('arial', self.text_size)

    def draw_screen(self, units, debug, hud):
        if not self.screen_open:
            self.start_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        self.display.fill(BACKGROUND_GRAY)
        for unit in units:

            pygame.draw.circle(self.display, unit.color, unit.position.values, unit.radius)

            if debug:
                pygame.draw.line(self.display, (0, 255, 0), unit.position.values, unit.destination.values, 1)
            if hud:
                # region IDs
                id = self.font.render(str(unit.id), True, WHITE)
                pos_text = unit.position.values
                pos_text[0] -= id.get_width()/2
                pos_text[1] += id.get_height()/2
                self.display.blit(id, pos_text)
                # endregion
                # region HEALTH
                pos_health = unit.position.values
                pos_health[1] -= unit.radius + self.health_bar_height + 5
                pos_health[0] -= self.health_bar_width/2
                rect = pygame.Rect(pos_health[0], pos_health[1],
                                   int(unit.health/unit.max_health * self.health_bar_width), self.health_bar_height)
                pygame.draw.rect(self.display, GREEN, rect)
                # endregion

        pygame.display.flip()

    def close_screen(self):
        pygame.quit()
        sys.exit()
