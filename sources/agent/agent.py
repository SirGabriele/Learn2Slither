import json
import random
import numpy as np
from pathlib import Path

from constants import GL_MODEL_DISCOUNT_FACTOR, GL_MODEL_LEARNING_RATE
from sources.enums.direction_enum import Direction


class Agent:
    def __init__(self,
                 sessions: int,
                 save_file: Path | None,
                 load_file: Path | None,
                 learning_mode: bool):
        self._save_file: Path | None = save_file
        self._load_file: Path | None = load_file
        self._learning_mode: bool = learning_mode
        self._qtable: dict[str, list[float | int]] = {}

        # Exploration rate.
        self._epsilon_max = 1.0
        self._epsilon = self._epsilon_max
        self._epsilon_min = 0.01

        # Geometric decay schedule designed to distribute exploration over
        # 100k sessions.
        # Target: Hit minimum floor (0.01) at exactly 80% of total training
        # (Session 80,000).
        #
        # --- Epsilon Evolution Timeline (100k Sessions) ---
        # Session 0      -> Epsilon = 1.00  (100% Random Exploration)
        # Session 1,830  -> Epsilon = 0.90  (90% Random, 10% Exploitation)
        # Session 5,000  -> Epsilon = 0.75  (75% Random, 25% Exploitation)
        # Session 12,041 -> Epsilon = 0.50  (50/50 Tipping Point)
        # Session 24,082 -> Epsilon = 0.25  (25% Random, 75% Exploitation)
        # Session 40,000 -> Epsilon = 0.10  (10% Random, 90% Exploitation)
        # Session 52,041 -> Epsilon = 0.05  (5% Random, 95% Exploitation)
        # Session 80,000 -> Epsilon = 0.01  (1% Random floor reached)
        # Session 100k   -> Epsilon = 0.01  (100% Exploitation)
        decay_horizon_sessions = max(1, int(sessions * 0.8))
        self.epsilon_decrease_factor = ((self._epsilon_min / self._epsilon_max)
                                        ** (1 / decay_horizon_sessions))

        if load_file:
            self.load(load_file)

        if save_file:
            self.save(save_file)

    #########################################################
    # ################## PROPERTIES $$$$#####################
    #########################################################

    @property
    def learning_mode(self) -> bool:
        return self._learning_mode

    #########################################################
    # ################## PUBLIC METHODS #####################
    #########################################################

    def load(self, load_file: Path):
        with open(load_file, "r") as file:
            self._qtable = json.load(file)

    def save(self, save_file: Path):
        with open(save_file, "w") as file:
            json.dump(self._qtable, file)

    def get_q_values(self, state_key: str) -> list[float | int]:
        if state_key not in self._qtable:
            self._qtable[state_key] = [0.0, 0.0, 0.0, 0.0]
        return self._qtable[state_key]

    def get_next_movement(self, game_state: str) -> Direction:
        # Exploration - Picks a random move.
        if (self._learning_mode
                and random.uniform(0, self._epsilon_max) < self._epsilon):
            action = random.choice(list(Direction))
        else:
            # Exploitation - Picks a move from the Q-Table.
            q_values = self.get_q_values(game_state)
            action_index = np.argmax(q_values)
            action = list(Direction)[action_index]

        return action

    def learn(self,
              old_game_state: str,
              new_game_state: str,
              reward: int,
              action: Direction,
              is_dead: bool):
        old_q_values = self.get_q_values(old_game_state)

        action_index = action.value
        current_q_value = old_q_values[action_index]

        if is_dead:
            max_future_q_values = 0.0
        else:
            new_q_values = self.get_q_values(new_game_state)
            # Gets the best possible reward from new state.
            max_future_q_values = np.max(new_q_values)

        # Bellman equation.
        new_q_value = current_q_value + GL_MODEL_LEARNING_RATE * (
                reward + GL_MODEL_DISCOUNT_FACTOR * max_future_q_values -
                current_q_value)

        self._qtable[old_game_state][action_index] = new_q_value

    def lower_epsilon(self):
        lowered_epsilon = self._epsilon * self.epsilon_decrease_factor
        self._epsilon = (lowered_epsilon
                         if lowered_epsilon >= self._epsilon_min
                         else self._epsilon_min)
