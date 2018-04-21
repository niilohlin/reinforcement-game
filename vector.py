
from typing import Tuple
from math import atan

class Vector:
    def __init__(self, x: float, y: float) -> None:
        self.x = x # type: float
        self.y = y # type: float

    def to_tuple(self) -> Tuple[float, float]:
        return (self.x, self.y)

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    @property
    def width(self) -> float:
        return self.x

    @property
    def height(self) -> float:
        return self.y

    @property
    def angle(self) -> float:
        return atan(self.y/self.x)


