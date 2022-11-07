import pygame, sys
from pygame.locals import *


class Screen:
    def __init__(self, horizontal_size, vertical_size, screen_name):
        pygame.init()
        self.horizontal_size = horizontal_size
        self.vertical_size = vertical_size
        self.screen_name = screen_name
        self.display = pygame.display.set_mode((self.horizontal_size, self.vertical_size))
        pygame.display.set_caption(self.screen_name)

        while True:
            self.draw_screen()

    def draw_screen(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

screen = Screen(1000, 500, "Test")