import pygame, sys
from pygame.locals import *
from Game.Unit import Unit
from Game.Type import Type


LINE = "-----------------------------------------------------------------------------"
BACKGROUND_GRAY = [100, 100, 100]


class Screen:
    def __init__(self, horizontal_size, vertical_size, screen_name):
        pygame.init()
        self.horizontal_size = horizontal_size
        self.vertical_size = vertical_size
        self.screen_name = screen_name
        self.display = pygame.display.set_mode((self.horizontal_size, self.vertical_size))
        pygame.display.set_caption(self.screen_name)

    def draw_screen(self):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()


units = list()
units.append(Unit(Type.SWORD, 1, 100, 100))
units.append(Unit(Type.HORSE, 2, 200, 100))
units.append(Unit(Type.SPEAR, 3, 300, 100))
units.append(Unit(Type.BOW, 4, 400, 100))

print("UNITS BEFORE MODIFICATIONS: ")
for unit in units:
    print()
    unit.test()

print(LINE)

print("UNITS BUFFED * 1.5: ")
for unit in units:
    unit.modify_stats(lambda x: x*1.5)
    print()
    unit.test()

print(LINE)

print("UNITS WITH ATTRIBUTES RESTORED: ")
for unit in units:
    unit.restore_stats()
    print()
    unit.test()

print(LINE)

print("TESTING EXCEPTIONS CREATING UNITS")
try:
    units.append(Unit("hulahula", 123, 0, 0))
except Exception as e:
    print(e)

screen = Screen(1000, 500, "TEST")
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        screen.display.fill(BACKGROUND_GRAY)
        for unit in units:
            pygame.draw.circle(screen.display, unit.color, [unit.x, unit.y], 5)
        pygame.display.flip()


