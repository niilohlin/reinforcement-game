
from typing import List, TYPE_CHECKING, Dict
from vector import *
from rect import *
from utils import any

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
        self.score = {left_player: 0, right_player: 0} # type: Dict[Player, int]


    def restart(self) -> None:
        from player import Player, PLAYER_WIDTH, PLAYER_HEIGHT
        self.players[0].frame.origin = Vector(PLAYER_WIDTH * 2, self.floor.origin.y - PLAYER_HEIGHT)
        self.players[1].frame.origin = Vector(GAME_WIDTH - PLAYER_WIDTH * 3, self.floor.origin.y - PLAYER_HEIGHT)
        for player in self.players:
            player.vel = Vector(0, 0)

    @property
    def is_running(self) -> bool:
        return not any(lambda player: self.score[player] >= 10, self.players)

    def _update_players(self) -> None:
        for player in self.players:
            player.update()

    def _detect_collision(self) -> None:
        winner = self.players[0].detect_collision_and_bounce(self.players[1])
        if winner:
            self.score[winner] += 1
            self.restart()
            return

        winner = self.players[1].detect_collision_and_bounce(self.players[0])
        if winner:
            self.score[winner] += 1
            self.restart()

    def _detect_walls(self) -> None:
        for player in self.players:
            player.bounce_walls()

    def update(self) -> None:
        self._update_players()
        self._detect_collision()
        self._detect_walls()
