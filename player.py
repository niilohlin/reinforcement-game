
from vector import Vector
from rect import Rect
from utils import sign
from typing import Optional, TYPE_CHECKING, Tuple
from copy import copy
import numpy as np

PLAYER_WIDTH = 40  # type: float
PLAYER_HEIGHT = 100  # type: float

if TYPE_CHECKING:
    from game import Game  # noqa F401


class Player:
    def __init__(self, game: 'Game', start_x: float, start_y: float) -> None:
        self.frame = Rect(start_x,
                          start_y,
                          PLAYER_WIDTH,
                          PLAYER_HEIGHT)  # type: Rect
        self.original_start_pos = Vector(start_x, start_y)  # type: Vector
        self.vel = Vector(0, 0)  # type: Vector
        self._game = game  # type: Game
        self._max_speed = 5  # type: float
        self._acceleration = 0.5  # type: float
        self.max_dash_ticks = 60 * 3  # type: int
        self.ticks_until_dash_ability = 0  # type: int

    def _update_pos(self) -> None:
        self.frame.origin += self.vel

    def reset(self) -> None:
        self.frame.origin = copy(self.original_start_pos)
        self.vel = Vector(0, 0)
        self.ticks_until_dash_ability = 0

    def update(self) -> None:
        self._apply_gravity()
        self._stand_on_floor()
        self._update_pos()
        self._deaccelerate()
        self._update_dash()

    def jump(self) -> None:
        if self.is_on_floor:
            self.vel.y -= 10

    def left(self) -> None:
        if self.vel.x > -self._max_speed:
            self.vel.x -= self._acceleration

    def right(self) -> None:
        if self.vel.x < self._max_speed:
            self.vel.x += self._acceleration

    def dash(self) -> None:
        if self.can_dash:
            self.vel.x *= 3
            self.ticks_until_dash_ability = self.max_dash_ticks

    @property
    def is_on_floor(self) -> bool:
        return self.frame.bottom >= self._game.floor.top

    @property
    def can_dash(self) -> bool:
        return self.ticks_until_dash_ability <= 0

    def _update_dash(self) -> None:
        self.ticks_until_dash_ability = max(0,
                                            self.ticks_until_dash_ability - 1)

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
            self.frame.origin.y = min(self._game.floor.top,
                                      self.frame.bottom) \
                - self.frame.size.height

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

    def detect_collision_and_bounce(self, other: 'Player') \
            -> Tuple[Optional['Player'], bool]:

        for frame in [other.frame, other._next_x_rect]:
            if self.frame.intersects(frame) or \
                    self._next_x_rect.intersects(frame):
                self._snap_horizontally_to_rect(frame)
                self.vel.x, other.vel.x = other.vel.x, self.vel.x
                return (None, True)

        for frame in [other.frame, other._next_y_rect]:
            if self.frame.intersects(frame) or \
                    self._next_y_rect.intersects(frame):
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
                return (winner, True)

        return (None, False)

    def bounce_walls(self) -> None:
        colliding_wall = None
        for wall in self._game.walls:
            if self._next_x_rect.intersects(wall):
                colliding_wall = wall
                break
        if colliding_wall:
            self._snap_horizontally_to_rect(colliding_wall)
            self.vel.x *= -1

    @property
    def to_array(self):
        return np.hstack([self.frame.to_array,
                         self.vel.to_array,
                         [self.ticks_until_dash_ability]]).flatten()
