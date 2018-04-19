
from typing import *

from player import *
from vector import *
from rect import *

GAME_WIDTH = 800 # type: int
GAME_HEIGHT = 600 # type: int

class Game:
    def __init__(self) -> None:
        self.players = [Player(), Player()] # type: List[Player]
        left_wall = Rect(0, 0, PLAYER_WIDTH, GAME_HEIGHT)
        right_wall = Rect(GAME_WIDTH - PLAYER_WIDTH, 0, PLAYER_WIDTH, GAME_HEIGHT)
        self.walls = [left_wall, right_wall] # type: List[Rect]
        self.floor = Rect(0, GAME_HEIGHT - int(GAME_HEIGHT / 3), GAME_WIDTH, GAME_HEIGHT) # type: Rect

    @property
    def is_running(self) -> bool:
        return True

