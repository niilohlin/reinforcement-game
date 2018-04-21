
from vector import *
from typing import Iterator, Optional

class Rect:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.origin = Vector(x, y) # type: Vector
        self.size = Vector(width, height) # type: Vector

    @property
    def bottom(self) -> float:
        return self.origin.y + self.size.height

    @property
    def top(self) -> float:
        return self.origin.y

    @property
    def left(self) -> float:
        return self.origin.x

    @property
    def right(self) -> float:
        return self.origin.x + self.size.width

    def covers(self, vector: Vector) -> bool:
        return self.left <= vector.x <= self.right and self.top <= vector.y <= self.bottom

    @property
    def _points(self) -> Iterator[Vector]:
        yield self.origin
        yield self.origin + Vector(self.size.width, 0)
        yield self.origin + Vector(0, self.size.height)
        yield self.origin + self.size

    def angle_between(self, other) -> float:
        return (self.origin - other.origin).angle

    def intersects(self, other: 'Rect', recurse: bool = True) -> Optional[float]:
        for point in other._points:
            if self.covers(point):
                return self.angle_between(other)
        if recurse:
            return other.intersects(self, False)
        return None
