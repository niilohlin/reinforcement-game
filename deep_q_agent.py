import random
import numpy as np
from collections import deque
from typing import Optional, Tuple, Deque, List

from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential

BATCH_SIZE: int = 128
EPISODES: int = 1500
EPISODE_LENGTH: int = 1000

ActionState = Tuple[np.ndarray, int, float, np.ndarray, bool]

class DeepQAgent:
    def __init__(self, n_state_features: int, n_actions: int, epsilon: float = 0.2) -> None:
        self.n_state_features: int = n_state_features
        self.n_actions: int = n_actions
        self.epsilon: float = epsilon

        # deque is a rolling buffer.
        self.memory: Deque[ActionState] = deque(maxlen=20000)
        self.learning_rate: float = 0.0001
        self.gamma: float = 0.9
        self.epsilon_decay: float = 0.999
        self.epsilon_min: float = 0.001
        self._model: Optional[Sequential] = None

    @property
    def model(self) -> Sequential:
        if self._model:
            return self._model

        model = Sequential()

        model.add(Dense(64, input_dim=self.n_state_features, activation='relu'))
        model.add(Dense(32, activation='relu'))
        model.add(Dense(16, activation='relu'))
        model.add(Dense(self.n_actions, activation='linear'))

        model.compile(loss='mean_squared_error', optimizer=Adam(lr=self.learning_rate))
        self._model = model
        return model

    def remember(self, state: np.ndarray, action: int, reward: float, next_state: np.ndarray, done: bool) -> None:
        self.memory.append((state, action, reward, next_state, done))

    def get_action(self, state: np.ndarray) -> int:
        if np.random.rand() <= self.epsilon:
            return random.randrange(self.n_actions)

        action_values = self.model.predict(state)
        best_action = np.argmax(action_values[0])

        return best_action

    def learn_from_memory(self, batch_size: int) -> None:
        batch: List[ActionState] = random.sample(self.memory, batch_size)

        for state, action, reward, next_state, terminated in batch:
            if not terminated:
                target: float = reward + self.gamma * np.amax(self.model.predict(next_state)[0])
            else:
                target = reward

            final_target: np.ndarray = self.model.predict(state)

            final_target[0][action] = target

            self.model.fit(state, final_target, epochs=1, verbose=0)

        self.epsilon = max(self.epsilon_min, self.epsilon_decay * self.epsilon)

    def load(self, name: str) -> None:
        self.model.load_weights(name)

    def save(self, name: str) -> None:
        self.model.save_weights(name)
