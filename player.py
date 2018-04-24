
from vector import *
from rect import *
from utils import sign, any
from typing import Optional, TYPE_CHECKING
from math import atan

PLAYER_WIDTH = 40 # type: float
PLAYER_HEIGHT = 100 # type: float


if TYPE_CHECKING:
    from game import Game

class Player:
    def __init__(self, game: 'Game', start_x: float, start_y: float) -> None:
        self.frame = Rect(start_x, start_y, PLAYER_WIDTH, PLAYER_HEIGHT) # type: Rect
        self.vel = Vector(0, 0) # type: Vector
        self._game = game # type: Game
        self._max_speed = 5 # type: float
        self._acceleration = 0.5 # type: float

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

    @property
    def is_on_floor(self) -> bool:
        return self.frame.bottom >= self._game.floor.top

    def _deaccelerate(self) -> None:
        self.vel.x -= 0.1 * sign(self.vel.x)

        if abs(self.vel.x) > self._max_speed:
            self.vel.x -= 0.2 * sign(self.vel.x)
        if abs(self.vel.x) <= 0.1:
            self.vel.x = 0

    def _apply_gravity(self) -> None:
        self.vel.y += 0.3

    def _stand_on_floor(self) -> None:
        if self.is_on_floor:
            self.vel.y = min(0, self.vel.y)
            self.frame.origin.y = min(self._game.floor.top, self.frame.bottom) - self.frame.size.height

    @property
    def _next_x_rect(self) -> Rect:
        return self.frame.moved(Vector(self.vel.x, 0))

    @property
    def _next_y_rect(self) -> Rect:
        return self.frame.moved(Vector(0, self.vel.y))

    def _snap_horizontally_to_rect(self, rect: Rect) -> None:
        if self.frame.left < rect.left:
            self.frame.origin.x = rect.origin.x - self.frame.size.width
        elif self.frame.left > rect.left:
            self.frame.origin.x = rect.right


    def _snap_vertically_to_rect(self, rect: Rect) -> None:
        if self.frame.top < rect.top:
            self.frame.origin.y = rect.origin.y - self.frame.size.height
        elif self.frame.top > rect.top:
            self.frame.origin.y = rect.bottom


    def detect_collision_and_bounce(self, other: 'Player') -> Optional['Player']:

        for frame in [other.frame, other._next_x_rect]:
            if self.frame.intersects(frame) or self._next_x_rect.intersects(frame):
                self._snap_horizontally_to_rect(frame)
                self.vel.x, other.vel.x = other.vel.x, self.vel.x
                return None

        for frame in [other.frame, other._next_y_rect]:
            if self.frame.intersects(frame) or self._next_y_rect.intersects(frame):
                self._snap_vertically_to_rect(frame)

                if self.vel.y - other.vel.y > 0:
                    winner = self
                else:
                    winner = other

                if other.is_on_floor:
                    self.vel.y *= -1
                elif self.is_on_floor:
                    other.vel.y *= -1
                else:
                    self.vel.y, other.vel.y = other.vel.y, self.vel.y
                return winner

        return None

    def bounce_walls(self) -> None:
        colliding_wall = list(filter(lambda wall: self._next_x_rect.intersects(wall), self._game.walls))
        if colliding_wall:
            self._snap_horizontally_to_rect(colliding_wall[0])
            self.vel.x *= -1

