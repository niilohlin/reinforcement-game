
from vector import *
from rect import *
from game import Game
from utils import sign

PLAYER_WIDTH = 40 # type: float
PLAYER_HEIGHT = 100 # type: float

class Player:
    def __init__(self, game: Game, start_x: float, start_y: float) -> None:
        self.frame = Rect(start_x, start_y, PLAYER_WIDTH, PLAYER_HEIGHT) # type: Rect
        self.vel = Vector(0, 0) # type: Vector
        self._game = game # type: Game
        self._max_speed = 5
        self._acceleration = 0.5

    def _update_pos(self) -> None:
        self.frame.origin += self.vel

    def update(self) -> None:
        self._apply_gravity()
        self._stand_on_floor()
        self._update_pos()
        self._deaccelerate()

    def jump(self) -> None:
        if self.is_on_floor:
            self.vel.y -= 10

    def left(self) -> None:
        if self.vel.x > -self._max_speed:
            self.vel.x -= self._acceleration

    def right(self) -> None:
        if self.vel.x < self._max_speed:
            self.vel.x += self._acceleration

    def _deaccelerate(self) -> None:
        self.vel.x -= 0.1 * sign(self.vel.x)

        if abs(self.vel.x) > self._max_speed:
            self.vel.x -= 0.2 * sign(self.vel.x)

    @property
    def is_on_floor(self) -> bool:
        return self.frame.bottom >= self._game.floor.top

    def _apply_gravity(self) -> None:
        self.vel.y += 0.3

    def _stand_on_floor(self) -> None:
        if self.is_on_floor:
            self.vel.y = min(0, self.vel.y)
            self.frame.origin.y = min(self._game.floor.top, self.frame.bottom) - self.frame.size.height
