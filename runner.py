
from typing import Iterable, Optional, Tuple
from game import Game
from view import View
from controller import Controller

class Runner:
    def __init__(self, game: Game, controllers: Iterable[Controller], view: Optional[View]) -> None:
        self.game = game  # type: Game
        self.controllers = controllers  # type: Iterable
        self.view = view  # type: Optional[View]

    def run(self):
        while self.game.is_running:

            if self.view:
                keys = self.view.get_keys()  # type: Optional[Tuple]
            else:
                keys = None

            for controller in self.controllers:
                controller.control(self.game, keys)

            self.game.update()

            self.view.draw(self.game)

        for controller in self.controllers:
            controller.control(self.game, keys)
