import numpy as np

from constants import GL_PRINT_TERMINAL
from sources.enums.direction_enum import Direction


def print_snake_vision(board_array: np.ndarray, action: Direction | None =
None) -> None:
    # Concatenates all rows and prints them to avoid the native ndarray print
    # format [[' ', ...]]
    # TODO delete
    if GL_PRINT_TERMINAL is False:
        return

    if action is not None:
        print(action.name)

    for row in board_array:
        print(" ".join(row))
