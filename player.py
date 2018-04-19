
from vector import *
from rect import *

PLAYER_WIDTH = 40 # type: float
PLAYER_HEIGHT = 100 # type: float

class Player:
    def __init__(self, start_x: float, start_y: float) -> None:
        self.frame = Rect(start_x, start_y, PLAYER_WIDTH, PLAYER_HEIGHT) # type: Rect
        self.vel = Vector(0, 0) # type: Vector

    def _update_pos(self) -> None:
        self.frame.origin += self.vel

    def update(self) -> None:
        self._update_pos()

