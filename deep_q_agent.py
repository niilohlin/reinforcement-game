import random
import numpy as np
from collections import deque
from typing import Optional, Tuple, Deque, List

from keras.layers import Dense
from keras.optimizers import Adam
from keras.models import Sequential

BATCH_SIZE = 128  # type: int
EPISODES = 1500  # type: int
EPISODE_LENGTH = 1000  # type: int

ActionState = Tuple[np.ndarray, int, float, np.ndarray, bool]

class DeepQAgent:
    def __init__(self, n_state_features: int, n_actions: int, epsilon: float = 1.0) -> None:
        self.n_state_features = n_state_features  # type: int
        self.n_actions = n_actions  # type: int
        self.epsilon = epsilon  # type: float

        # deque is a rolling buffer.
        self.memory = deque(maxlen=20000)  # type: Deque[ActionState]
        self.learning_rate = 0.0001  # type: float
        self.gamma = 0.9  # type: float
        self.epsilon_decay = 0.999  # type: float
        self.epsilon_min = 0.001  # type: float
        self._model = None  # type: Optional[Sequential]

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
        batch = random.sample(self.memory, batch_size)  # type: List[ActionState]

        for state, action, reward, next_state, terminated in batch:
            if not terminated:
                target = reward + self.gamma * np.amax(self.model.predict(next_state)[0])  # type: float
            else:
                target = reward

            final_target = self.model.predict(state)  # type: np.ndarray

            final_target[0][action] = target

            self.model.fit(state, final_target, epochs=1, verbose=0)

        self.epsilon = min(self.epsilon_min, self.epsilon_decay * self.epsilon)

    def load(self, name: str) -> None:
        self.model.load_weights(name)

    def save(self, name: str) -> None:
        self.model.save_weights(name)
