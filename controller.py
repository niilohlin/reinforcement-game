
from typing import Optional, Tuple
from typing_extensions import Protocol, runtime
from game import Game


@runtime
class Controller(Protocol):
    def control(self, game: Game, keys: Tuple) -> None:
        ...
