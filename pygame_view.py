
import pygame
import sys
import time
import os
import random
from game import *
from keyboard_controller import KeyboardController
from random_controller import RandomController

from pygame.locals import RLEACCEL, QUIT, K_r, K_SPACE, K_UP, K_LEFT, K_RIGHT, K_w, K_d, K_a, K_e


class PygameView:
    def __init__(self, game, controllers):
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((255,255,255))
        self.clock = pygame.time.Clock()
        self.game = game
        self.controllers = controllers
        pygame.key.set_repeat(1, 1)


    def fill_rect(self, rect, color):
        surface = pygame.Surface(rect.size.to_tuple())
        surface.fill(color)
        self.screen.blit(surface, rect.origin.to_tuple())

    def draw_score(self):
        font = pygame.font.Font(None, 14)
        text = font.render("{} - {}".format(self.game.score[self.game.players[0]], self.game.score[self.game.players[1]]), 1, (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = GAME_WIDTH / 2
        self.screen.blit(text, textpos)
        pass

    def draw_game(self):
        self.fill_rect(self.game.floor, (0, 0, 0))
        self.fill_rect(self.game.walls[0], (0, 0, 0))
        self.fill_rect(self.game.walls[1], (0, 0, 0))
        self.fill_rect(self.game.players[0].frame, (100, 100, 100))
        self.fill_rect(self.game.players[1].frame, (100, 100, 100))
        self.draw_score()

    def run(self):
        while self.game.is_running:
            pygame.event.pump()
            keys = pygame.key.get_pressed()

            for event in pygame.event.get():

                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

            for controller in self.controllers:
                controller.control(self.game, keys)
            self.game.update()

            self.surface.fill((255,255,255))
            self.screen.blit(self.surface, (0,0))
            self.draw_game()

            pygame.display.flip()
            pygame.display.update()

            self.fpsClock.tick(self.FPS) # and tick the clock.
