
from vector import *
from rect import *
from game import Game
from utils import sign
from typing import Optional
from math import atan

PLAYER_WIDTH = 40 # type: float
PLAYER_HEIGHT = 100 # type: float

class Player:
    def __init__(self, game: Game, start_x: float, start_y: float) -> None:
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

    def detect_collision_and_bounce(self, rect: Rect) -> Optional[float]:
        angle = self.frame.intersects(rect)
        if not angle:
            return None

        print("atan(rect.size.angle)       = " + str(atan(rect.size.angle)))
        print("atan(self.frame.size.angle) = " + str(atan(self.frame.size.angle)))
        print("angle                       = " + str(angle)) # 1.3887088178733646
        #0.8581339435835402

#        if atan(rect.size.angle) > angle or angle > atan(self.frame.size.angle):
#            print("stomp")
#            self.vel.y *= -1
#            self.frame.origin.y = rect.origin.y - self.frame.size.height - 1
#
#        if angle < atan(self.frame.size.angle):
#            print("side 1")
#            self.vel.x *= -1
#
#        if angle > atan(rect.size.angle):
#            print("side 2")
#            self.vel.x *= -1

        return angle

