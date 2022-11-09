import pygame, sys
from pygame.locals import *
from Game.GameState import GameState


BACKGROUND_GRAY = [100, 100, 100]


class Screen:
    def __init__(self, horizontal_size, vertical_size, screen_name):
        pygame.init()
        self.horizontal_size = horizontal_size
        self.vertical_size = vertical_size
        self.screen_name = screen_name
        self.display = pygame.display.set_mode((self.horizontal_size, self.vertical_size))
        pygame.display.set_caption(self.screen_name)

    def draw_screen(self, units):
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            self.display.fill(BACKGROUND_GRAY)
            for unit in units:
                pygame.draw.circle(self.display,[0,0,0], [unit.x, unit.y], 5)
            pygame.display.flip()


class Game:
    def __init__(self, parameters):
        self.game_state = GameState(parameters)
        self.reset()
        self.screen = Screen(parameters.screen_width,
                             parameters.screen_height, "TotalBotWar")  # Just for pygame version

    def reset(self):
        """Reset GameState so is ready for a new 'Game'"""
        self.game_state.reset()

    def run(self, player1: "TotalBotWar.Players.Player.Player", player2: "TotalBotWar.Players.Player.Player",
            verbose: bool, budged: float):
        """Runs a TotalBotWar 'Game'"""
        players = [player1, player2]
        for unit in self.game_state.player_0_units:
            print(unit, "\n")
        print("--------------------------------------------------------")
        for unit in self.game_state.player_1_units:
            print(unit, "\n")
        while not self.game_state.is_terminal():
            # self.play_turn(players[self.game_state.turn])
            self.screen.draw_screen(self.game_state.player_0_units +
                                    self.game_state.player_1_units)  # Just for pygame version
