from typing import Optional, Tuple
from typing_extensions import Protocol, runtime
from game import Game


@runtime
class View(Protocol):
    def draw(self, game: Game) -> None:
        ...

    def get_keys(self) -> Optional[Tuple]:
        ...

