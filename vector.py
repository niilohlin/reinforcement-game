
from typing import *

class Vector:
    def __init__(self, x: int, y: int) -> None:
        self.x = x # type: int
        self.y = y # type: int

    def to_tuple(self) -> Tuple[int, int]:
        return (self.x, self.y)

class Size:
    def __init__(self, width: int, height: int) -> None:
        self.width = width # type: int
        self.height = height # type: int

    def to_tuple(self) -> Tuple[int, int]:
        return (self.width, self.height)

