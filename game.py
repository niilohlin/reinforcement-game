
from typing import List, Dict, Optional # noqa F401
from rect import Rect
from utils import any
from player import Player, PLAYER_WIDTH, PLAYER_HEIGHT
from itertools import permutations
import numpy as np

GAME_WIDTH: float = 800
GAME_HEIGHT: float = 600


class Game:
    def __init__(self) -> None:
        self.floor: Rect = Rect(0,
                          GAME_HEIGHT - float(GAME_HEIGHT / 3),
                          GAME_WIDTH,
                          GAME_HEIGHT)

        left_player = Player(self,
                             PLAYER_WIDTH * 2,
                             self.floor.origin.y - PLAYER_HEIGHT)
        right_player = Player(self,
                              GAME_WIDTH - PLAYER_WIDTH * 3,
                              self.floor.origin.y - PLAYER_HEIGHT)

        self.players: List[Player] = [left_player, right_player]
        left_wall = Rect(0, 0, PLAYER_WIDTH, GAME_HEIGHT)
        right_wall = Rect(GAME_WIDTH - PLAYER_WIDTH,
                          0,
                          PLAYER_WIDTH,
                          GAME_HEIGHT)
        self.walls: List[Rect] = [left_wall, right_wall]
        self.score: Dict[Player, int] = {left_player: 0, right_player: 0}
        self._max_score: int = 10

    def restart(self) -> None:
        for player in self.players:
            player.reset()

    @property
    def winner(self) -> Optional[Player]:
        for player in self.players:
            if self.score[player] == self._max_score:
                return player
        return None

    @property
    def is_running(self) -> bool:
        return not any(lambda player: self.score[player] >= self._max_score, self.players)

    def _update_players(self) -> None:
        for player in self.players:
            player.update()

    def _detect_collision(self) -> None:
        for (player1, player2) in permutations(self.players):
            (winner, did_collide) = player1.\
                                    detect_collision_and_bounce(player2)
            if winner:
                self.score[winner] += 1
                self.restart()
                return
            if did_collide:
                break

    def _detect_walls(self) -> None:
        for player in self.players:
            player.bounce_walls()

    def update(self) -> None:
        self._update_players()
        self._detect_collision()
        self._detect_walls()

    @property
    def to_array(self):
        player_arrays = np.array([])
        for player in self.players:
            player_arrays = np.append(player_arrays, player.to_array)
        return player_arrays
