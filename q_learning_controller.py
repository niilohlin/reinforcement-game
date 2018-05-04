
from typing import Tuple, Optional, Dict

from player import Player
from game import Game
import numpy as np
from deep_q_agent import DeepQAgent, BATCH_SIZE
import os.path


class QLearningController:
    def __init__(self, player: Player, player_name: str = 'reinforcement_game') -> None:
        self.player: Player = player
        self.player_name: str = player_name

        n_actions: int = len(player.all_actions)
        # hard coded for now. The length of the game state.
        n_state_features: int = 14
        self.agent: DeepQAgent = DeepQAgent(n_state_features, n_actions)

        if os.path.isfile(f'./models/{self.player_name}.h5'):
            self.agent.load(f'./models/{self.player_name}.h5')
        self._previous_state: Optional[np.ndarray] = None
        self._previous_player_score: Optional[int] = None
        self._previous_other_score: Optional[int] = None
        self._previous_action: Optional[int] = None
        self._episode: int = 0

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
            return 10
        if game.score[other_player] > self._previous_other_score:
            self._previous_other_score = game.score[other_player]
            return -10

        return 0

    def _other_player(self, game: Game) -> Optional[Player]:
        for player in game.players:
            if player != self.player:
                return player
        return None

    def control(self, game: Game, keys: Tuple) -> None:
        self._episode += 1
        if not game.is_running or self._episode % 100 == 0:
            self.agent.save(f'./models/{self.player_name}.h5')
            return

        current_state = game.to_array
        current_state = np.reshape(current_state, [1, 14])
        action: int = self.agent.get_action(current_state)

        if self._previous_state is None or self._previous_action is None:
            self._previous_state = current_state
            self.player.all_actions[action]()
            self._previous_action = action
            return

        reward_for_previous_action: float = self._get_reward(game)

        self.player.all_actions[action]()
        new_state = game.to_array
        new_state = np.reshape(new_state, [1, 14])

        self.agent.remember(self._previous_state, self._previous_action, reward_for_previous_action, new_state, not game.is_running)

        self._previous_state = new_state

        if len(self.agent.memory) >= BATCH_SIZE:
            self.agent.learn_from_memory(BATCH_SIZE)
        print("epsilon: " + str(self.agent.epsilon) + " episode: " + str(self._episode))
