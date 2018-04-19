
from typing import Tuple

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

class Size:
    def __init__(self, width: float, height: float) -> None:
        self.width = width # type: float
        self.height = height # type: float

    def to_tuple(self) -> Tuple[float, float]:
        return (self.width, self.height)

