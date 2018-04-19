
from vector import *

class Rect:
    def __init__(self, x: int, y: int, width: int, height: int) -> None:
        self.origin = Vector(x, y) # type: Vector
        self.size = Size(width, height) # type: Size
