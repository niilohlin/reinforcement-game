
from vector import *

class Rect:
    def __init__(self, x: float, y: float, width: float, height: float) -> None:
        self.origin = Vector(x, y) # type: Vector
        self.size = Size(width, height) # type: Size

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
