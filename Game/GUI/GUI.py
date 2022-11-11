import pygame, sys
from pygame.locals import *

BACKGROUND_GRAY = [100, 100, 100]


class GUI:
    def __init__(self, screen_size, screen_name):
        self.screen_size = screen_size
        self.screen_name = screen_name
        self.display = None
        self.screen_open = False

    def start_screen(self):
        pygame.init()
        self.display = pygame.display.set_mode(self.screen_size)
        pygame.display.set_caption(self.screen_name)
        self.screen_open = True

    def draw_screen(self, units):
        if not self.screen_open:
            self.start_screen()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        self.display.fill(BACKGROUND_GRAY)
        for unit in units:
            pygame.draw.circle(self.display, unit.color, [unit.x, unit.y], unit.radius)
            pygame.draw.line(self.display, (0, 255, 0), (unit.x, unit.y), unit.destination, 1)
        pygame.display.flip()

    def close_screen(self):
        pygame.quit()
        sys.exit()
