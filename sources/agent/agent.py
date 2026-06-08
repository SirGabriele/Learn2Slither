import json
import random
import numpy as np
from pathlib import Path

from sources.enums.direction_enum import Direction


class Agent:
    def __init__(self,
                 save_file: Path | None,
                 load_file: Path | None,
                 learning_mode: bool):
        self.save_file: Path | None = save_file
        self.load_file: Path | None = load_file
        self.learning_mode: bool = learning_mode
        self.qtable: dict[str, list[float]] = {}

        self.learning_rate = 0.1

        self.discount_factor = 0.9

        # Exploration rate
        self.epsilon = 0.1
        self.epsilon_max = 1.0
        self.epsilon_min = 0.01

        # Multiply epsilon by this after every game
        self.epsilon_decrease_factor = 0.995

        if load_file:
            self.load(load_file)

        if save_file:
            self.save(save_file)

    def load(self, load_file: Path):
        with open(load_file, "r") as file:
            self.qtable = json.load(file)

    def save(self, save_file: Path):
        with open(save_file, "w") as file:
            json.dump(self.qtable, file)

    def get_q_values(self, state_key: str) -> list[float]:
        if state_key not in self.qtable:
            self.qtable[state_key] = [0.0, 0.0, 0.0, 0.0]
        return self.qtable[state_key]

    def get_next_movement(self, game_state: str) -> Direction:
        # Exploration - Picks a random move
        if self.learning_mode and \
                random.uniform(0, self.epsilon_max) < self.epsilon:
            action = random.choice(list(Direction))
        else:
            # Exploitation - Picks a move from the Q-Table
            q_values = self.get_q_values(game_state)
            action_index = np.argmax(q_values)
            action = list(Direction)[action_index]

        return action

    def learn(self,
              old_game_state: str,
              new_game_state: str,
              reward: int,
              action: Direction):
        old_q_values = self.get_q_values(old_game_state)
        new_q_values = self.get_q_values(new_game_state)

        action_index = action.value
        current_q_value = old_q_values[action_index]

        # What is the best possible score from the new state?
        max_future_q_values = np.max(new_q_values)

        # THE BELLMAN EQUATION
        new_q = current_q_value + self.learning_rate * (
                reward + self.discount_factor * max_future_q_values - current_q_value)

        self.qtable[old_game_state][action_index] = new_q

    def lower_epsilon(self):
        self.epsilon = self.epsilon * self.epsilon_decrease_factor
