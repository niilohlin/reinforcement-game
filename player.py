
from vector import *
from rect import *

PLAYER_WIDTH = 40
PLAYER_HEIGHT = 100

class Player:
    def __init__(self) -> None:
        self.frame = Rect(0, 0, PLAYER_WIDTH, PLAYER_HEIGHT) # type: Rect
        self.vel = Vector(0, 0) # type: Vector

