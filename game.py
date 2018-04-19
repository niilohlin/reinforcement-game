
from typing import List

from player import *
from vector import *
from rect import *

GAME_WIDTH = 800 # type: float
GAME_HEIGHT = 600 # type: float

class Game:
    def __init__(self) -> None:
        self.floor = Rect(0, GAME_HEIGHT - float(GAME_HEIGHT / 3), GAME_WIDTH, GAME_HEIGHT) # type: Rect

        left_player = Player(PLAYER_WIDTH * 2, self.floor.origin.y - PLAYER_HEIGHT)
        right_player = Player(GAME_WIDTH - PLAYER_WIDTH * 3, self.floor.origin.y - PLAYER_HEIGHT)

        self.players = [left_player, right_player] # type: List[Player]
        left_wall = Rect(0, 0, PLAYER_WIDTH, GAME_HEIGHT)
        right_wall = Rect(GAME_WIDTH - PLAYER_WIDTH, 0, PLAYER_WIDTH, GAME_HEIGHT)
        self.walls = [left_wall, right_wall] # type: List[Rect]

    @property
    def is_running(self) -> bool:
        return True

    def _apply_gravity(self) -> None:
        for player in self.players:
            player.vel.y += 0.3

    def _player_is_on_floor(self, player) -> bool:
        return player.frame.bottom >= self.floor.top

    def _stand_on_floor(self) -> None:
        for player in self.players:
            if self._player_is_on_floor(player):
                player.vel.y = min(0, player.vel.y)
                player.frame.origin.y = min(self.floor.top, player.frame.bottom) - player.frame.size.height

    def _update_players(self) -> None:
        for player in self.players:
            player.update()

    def update(self) -> None:
        self._apply_gravity()
        self._stand_on_floor()
        self._update_players()
