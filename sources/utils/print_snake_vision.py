import numpy as np


def print_snake_vision(board_array: np.ndarray) -> None:
    # Concatenates all rows and prints them to avoid the native ndarray print
    # format [[' ', ...]]
    for row in board_array:
        print(" ".join(row))

    # Adds a newline to make the display more readable
    print()
