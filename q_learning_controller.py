
from typing import Tuple, Optional

from player import Player
from game import Game
import numpy as np
from deep_q_agent import DeepQAgent

class QLearningController:
    def __init__(self, player: Player) -> None:
        self.player = player  # type: Player

        n_actions = len(player.all_actions)  # type: int
        # hard coded for now. The length of the game state.
        n_state_features = 14  # type: int
        self.agent = DeepQAgent(n_state_features, n_actions)  # type: DeepQAgent
        self._previous_state = None  # type Optional[np.ndarray]

    def control(self, game: Game, keys: Tuple) -> None:
        if not game.is_running:
            return

        current_state = game.to_array
        action = self.agent.get_action(current_state)  # type: int

        if not self._previous_state:
            self._previous_state = current_state
            self.player.all_actions[action]()
            return





        pass


