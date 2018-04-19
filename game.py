
from typing import List

from vector import *
from rect import *

GAME_WIDTH = 800 # type: float
GAME_HEIGHT = 600 # type: float

class Game:
    def __init__(self) -> None:
        from player import Player, PLAYER_WIDTH, PLAYER_HEIGHT
        self.floor = Rect(0, GAME_HEIGHT - float(GAME_HEIGHT / 3), GAME_WIDTH, GAME_HEIGHT) # type: Rect

        left_player = Player(self, PLAYER_WIDTH * 2, self.floor.origin.y - PLAYER_HEIGHT)
        right_player = Player(self, GAME_WIDTH - PLAYER_WIDTH * 3, self.floor.origin.y - PLAYER_HEIGHT)

        self.players = [left_player, right_player] # type: List[Player]
        left_wall = Rect(0, 0, PLAYER_WIDTH, GAME_HEIGHT)
        right_wall = Rect(GAME_WIDTH - PLAYER_WIDTH, 0, PLAYER_WIDTH, GAME_HEIGHT)
        self.walls = [left_wall, right_wall] # type: List[Rect]

    @property
    def is_running(self) -> bool:
        return True

    def _update_players(self) -> None:
        for player in self.players:
            player.update()

    def update(self) -> None:
        self._update_players()
