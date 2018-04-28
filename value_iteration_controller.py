
from typing import Tuple, List

from player import Player
from game import Game
import numpy as np


class QLearningController:
    def __init__(self, player: Player) -> None:
        self.player = player  # type: Player
        self.moves = []  # type: List

    def control(self, game: Game, keys: Tuple) -> None:
        pass

