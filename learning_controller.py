
from typing import Tuple

from player import Player
from game import Game
import numpy as np

class LearningController:
    def __init__(self, player: Player) -> None:
        self.player = player

    def control(self, game: Game, keys: Tuple) -> None:
        pass
