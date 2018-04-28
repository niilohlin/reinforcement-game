
from typing import Tuple

from player import Player
from game import Game
from random import choice
from controller import Controller

class RandomController(Controller):
    def __init__(self, player: Player) -> None:
        self.player = player

    def control(self, game: Game, keys: Tuple) -> None:
        if not game.is_running:
            return
        choice([self.player.jump, self.player.right, self.player.left, self.player.dash, self.player.idle])()
