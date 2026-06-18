import numpy as np

from constants import GL_PRINT_TERMINAL
from sources.enums.direction_enum import Direction


def print_snake_vision(cross_view: np.ndarray,
                       action: Direction | None = None) -> None:
    if not GL_PRINT_TERMINAL:
        return

    if action is not None:
        print(action.name)
        print()

    # Concatenates all rows and prints them to avoid the native ndarray print
    # format [[' ', ...]]
    for row in cross_view:
        print(" ".join(row))

    print()
