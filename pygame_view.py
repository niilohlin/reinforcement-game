
import pygame
import sys
from game import Game, GAME_WIDTH, GAME_HEIGHT
from vector import Vector
from rect import Rect
from pygame.locals import QUIT
from view import View
from typing import Optional, Tuple


class PygameView(View):
    def __init__(self, game):
        self.FPS = 60
        self.fpsClock = pygame.time.Clock()

        self.screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT), 0, 32)
        self.surface = pygame.Surface(self.screen.get_size())
        self.surface = self.surface.convert()
        self.surface.fill((255, 255, 255))
        self.clock = pygame.time.Clock()
        self.game = game
        pygame.key.set_repeat(1, 1)

    def fill_rect(self, rect, color):
        surface = pygame.Surface(rect.size.to_tuple())
        surface.fill(color)
        self.screen.blit(surface, rect.origin.to_tuple())

    def draw_score(self):
        font = pygame.font.Font(None, 18)
        text = font.render("{} - {}"
                           .format(self.game.score[self.game.players[0]],
                                   self.game.score[self.game.players[1]]),
                           1,
                           (10, 10, 10))
        textpos = text.get_rect()
        textpos.centerx = GAME_WIDTH / 2
        self.screen.blit(text, textpos)

    def draw_dash_bar(self, player, pos, direction):
        assert(direction == "left" or direction == "right")
        if direction == "left":
            self.fill_rect(
                    Rect(pos.x,
                         pos.y,
                         player.ticks_until_dash_ability /
                         player.max_dash_ticks * 300,
                         10),
                    (0, 0, 0)
            )
        elif direction == "right":
            dash_length = player.ticks_until_dash_ability /\
                    player.max_dash_ticks * 300
            self.fill_rect(
                    Rect(pos.x - dash_length,
                         pos.y,
                         dash_length,
                         10),
                    (0, 0, 0)
            )

    def draw_dash_bars(self):
        self.draw_dash_bar(self.game.players[0],
                           Vector(80, 10),
                           "left")
        self.draw_dash_bar(self.game.players[1],
                           Vector(GAME_WIDTH - 80, 10),
                           "right")

    def draw_game(self):
        self.fill_rect(self.game.floor, (0, 0, 0))
        self.fill_rect(self.game.walls[0], (0, 0, 0))
        self.fill_rect(self.game.walls[1], (0, 0, 0))
        self.fill_rect(self.game.players[0].frame, (100, 100, 100))
        self.fill_rect(self.game.players[1].frame, (100, 100, 100))
        self.draw_score()
        self.draw_dash_bars()

    def draw(self, game: Game) -> None:
        self.surface.fill((255, 255, 255))
        self.screen.blit(self.surface, (0, 0))
        self.draw_game()

        pygame.display.flip()
        pygame.display.update()

        self.fpsClock.tick(self.FPS)

    def get_keys(self) -> Optional[Tuple]:
        pygame.event.pump()
        keys = pygame.key.get_pressed()

        for event in pygame.event.get():

            if event.type == QUIT:
                pygame.quit()
                sys.exit()
        return keys
