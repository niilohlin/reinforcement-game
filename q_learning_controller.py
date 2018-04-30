
from typing import Tuple, Optional, Dict

from player import Player
from game import Game
import numpy as np
from deep_q_agent import DeepQAgent, BATCH_SIZE
import os.path

class QLearningController:
    def __init__(self, player: Player) -> None:
        self.player = player  # type: Player

        n_actions = len(player.all_actions)  # type: int
        # hard coded for now. The length of the game state.
        n_state_features = 14  # type: int
        self.agent = DeepQAgent(n_state_features, n_actions)  # type: DeepQAgent

        if os.path.isfile('./models/reinforcement_game.h5'):
            self.agent.load('./models/reinforcement_game.h5')
        self._previous_state = None  # type: Optional[np.ndarray]
        self._previous_player_score = None  # type: Optional[int]
        self._previous_other_score = None  # type: Optional[int]
        self._previous_action = None  # type: Optional[int]

    def _get_reward(self, game: Game) -> float:
        other_player = self._other_player(game)
        if not other_player:
            return 0

        if self._previous_player_score is None:
            self._previous_player_score = game.score[self.player]
        if self._previous_other_score is None:
            self._previous_other_score = game.score[other_player]

        if not game.is_running and game.winner == self.player:
            return 100
        if not game.is_running and game.winner != self.player:
            return -100

        if game.score[self.player] > self._previous_player_score:
            self._previous_player_score = game.score[self.player]
            return 1
        if game.score[other_player] > self._previous_other_score:
            self._previous_other_score = game.score[other_player]
            return -1

        return 0

    def _other_player(self, game: Game) -> Optional[Player]:
        for player in game.players:
            if player != self.player:
                return player
        return None

    def control(self, game: Game, keys: Tuple) -> None:
        if not game.is_running:
            self.agent.save('./models/reinforcement_game.h5')
            return

        current_state = game.to_array
        current_state = np.reshape(current_state, [1, 14])
        action = self.agent.get_action(current_state)  # type: int

        if self._previous_state is None or self._previous_action is None:
            self._previous_state = current_state
            self.player.all_actions[action]()
            self._previous_action = action
            return

        reward_for_previous_action = self._get_reward(game)  # type: float
        self.player.all_actions[action]()
        new_state = game.to_array
        new_state = np.reshape(new_state, [1, 14])

        self.agent.remember(new_state, self._previous_action, reward_for_previous_action, new_state, not game.is_running)

        self._previous_state = new_state

        if len(self.agent.memory) >= BATCH_SIZE:
            self.agent.learn_from_memory(BATCH_SIZE)
