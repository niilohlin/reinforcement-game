
from typing import Tuple

from player import Player
from game import Game
from pygame.locals import K_UP, K_LEFT, K_RIGHT, K_SPACE

class KeyboardController:
    def __init__(self, player: Player) -> None:
        self.player = player

    def control(self, game: Game, keys: Tuple) -> None:
        if keys[K_UP]:
            self.player.jump()
        if keys[K_RIGHT]:
            self.player.right()
        if keys[K_LEFT]:
            self.player.left()
        if keys[K_SPACE]:
            self.player.dash()
