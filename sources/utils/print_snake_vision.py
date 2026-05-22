import numpy as np

from constants import GL_PRINT_TERMINAL


def print_snake_vision(board_array: np.ndarray) -> None:
    # Concatenates all rows and prints them to avoid the native ndarray print
    # format [[' ', ...]]
    # TODO delete
    if GL_PRINT_TERMINAL is False:
        return

    for row in board_array:
        print(" ".join(row))

    # Adds a newline to make the display more readable
    print()
