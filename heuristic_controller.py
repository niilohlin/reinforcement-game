
from typing import Tuple

from player import Player
from game import Game
from controller import Controller

class HeuristicController(Controller):
    def __init__(self, player: Player) -> None:
        self.player = player

    def control(self, game: Game, keys: Tuple) -> None:
        if not game.is_running:
            return
        other_player: Player = list(filter(lambda player: player != self.player, game.players))[0]
        if other_player.frame.origin.x < self.player.frame.origin.x:
            self.player.left()
        else:
            self.player.right()
        self.player.jump()

