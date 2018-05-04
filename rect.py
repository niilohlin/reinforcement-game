
from vector import Vector
from typing import Iterator
import numpy as np

class Rect:
    def __init__(self, x: float, y: float, width: float, height: float)\
            -> None:
        self.origin: Vector = Vector(x, y)
        self.size: Vector = Vector(width, height)

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
        return self.left <= vector.x <= self.right and \
            self.top <= vector.y <= self.bottom

    def moved(self, vector: Vector) -> 'Rect':
        return Rect(self.origin.x + vector.x,
                    self.origin.y + vector.y,
                    self.size.width,
                    self.size.height)

    @property
    def points(self) -> Iterator[Vector]:
        yield self.origin
        yield self.origin + Vector(self.size.width, 0)
        yield self.origin + Vector(0, self.size.height)
        yield self.origin + self.size

    def intersects(self, other: 'Rect', recurse: bool = True) -> bool:
        for point in other.points:
            if self.covers(point):
                return True
        if recurse:
            return other.intersects(self, False)
        return False

    @property
    def to_array(self):
        return np.array([self.origin.to_array, self.size.to_array]).flatten()
