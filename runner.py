
from typing import Iterable, Optional, Tuple
from game import Game
from view import View
from controller import Controller
from q_learning_controller import QLearningController
from heuristic_controller import HeuristicController
from pygame_view import PygameView
from cli_view import CLIView


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


class LearningRunner:
    def __init__(self):
        self.game = Game()
        keyboard_controller = QLearningController(self.game.players[0])  # type: Controller
        heuristic_controller = HeuristicController(self.game.players[1])  # type: Controller
        self.view = PygameView(self.game)
        self.controllers = [heuristic_controller, keyboard_controller]

    def run(self):
        print("starting run")
        while self.game.is_running:

            for controller in self.controllers:
                controller.control(self.game, None)

            self.game.update()

            self.view.draw(self.game)

        for controller in self.controllers:
            controller.control(self.game, None)
