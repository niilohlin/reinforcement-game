
from typing import Tuple, Optional, Dict

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
        self._previous_state = None  # type: Optional[np.ndarray]
        self._previous_player_score = None  # type: Optional[int]
        self._previous_other_score = None  # type: Optional[int]
        self._previous_action = None  # type: Optional[int]


    def _get_reward(self, game: Game) -> float:
        if not game.is_running and game.winner == self.player:
            return 100
        if not game.is_running and game.winner != self.player:
            return -100

        if game.score[self.player] > self._previous_player_score:
            self._previous_player_score = game.score[self.player]
            return 1
        if game.score[self._other_player(game)] > self._previous_other_score:
            self._previous_other_score = game.score[self._other_player(game)]
            return -1

        return 0

    def _other_player(self, game: Game) -> Optional[Player]:
        for player in game.players:
            if player != self.player:
                return player
        return None


    def control(self, game: Game, keys: Tuple) -> None:
        if not game.is_running:
            return

        current_state = game.to_array
        action = self.agent.get_action(current_state)  # type: int

        if not self._previous_state:
            self._previous_state = current_state
            self.player.all_actions[action]()
            return



