
from typing import Tuple

from player import Player
from game import Game

class HeuristicController:
    def __init__(self, player: Player) -> None:
        self.player = player

    def control(self, game: Game, keys: Tuple) -> None:
        other_player = list(filter(lambda player: player != self.player, game.players))[0] # type: Player
        if other_player.frame.origin.x < self.player.frame.origin.x:
            self.player.left()
        else:
            self.player.right()
        self.player.jump()

