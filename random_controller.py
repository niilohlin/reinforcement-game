
from typing import Tuple

from player import Player
from game import Game
from random import choice

class RandomController:
    def __init__(self, player: Player) -> None:
        self.player = player

    def nothing(self) -> None:
        pass

    def control(self, game: Game, keys: Tuple) -> None:
        choice([self.player.jump, self.player.right, self.player.left, self.nothing])()
