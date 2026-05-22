import json

from bitmap import BitMap
from pathlib import Path
from numpy import ndarray

from sources.enums.direction_enum import Direction
from sources.utils.convert_game_state_to_bitmap import \
    convert_game_state_to_bitmap


class Agent:
    def __init__(self,
                 save_file: Path | None,
                 load_file: Path | None,
                 learning_mode: bool):
        self.save_file: Path | None = save_file
        self.load_file: Path | None = load_file
        self.learning_mode: bool = learning_mode
        self.qtable: dict[str, tuple[float, float, float, float]] = {}

        if load_file:
            self.load(load_file)

        if save_file:
            self.save(save_file)

    def load(self, load_file: Path):
        with open(load_file, "r") as file:
            data = json.load(file)

            for key, value in data.items():
                self.qtable[key] = value

    def save(self, save_file: Path):
        with open(save_file, "w") as file:
            json.dump(self.qtable, file)

    def get_next_movement(self, game_state: ndarray) -> Direction:
        bitmap: BitMap = convert_game_state_to_bitmap(game_state)
        print("bitmap is", bitmap.tostring())

        rewards = self.qtable.get(bitmap.tostring())
        if rewards is None:
            print("unknown state")
        else:
            print(rewards)

        # row, col = np.where(game_state == 'H')
        # if game_state[row, col + 1] != 'W':
        #     return Direction.LEFT
        return Direction.UP