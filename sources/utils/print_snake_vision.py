import numpy as np

from sources.enums.direction_enum import Direction


def print_snake_vision(cross_view: np.ndarray,
                       is_learning_mode: bool,
                       action: Direction | None = None) -> None:
    if is_learning_mode:
        return

    if action is not None:
        print(action.name)
        print()

    # Concatenates all rows and prints them to avoid the native ndarray print
    # format [[' ', ...]]
    for row in cross_view:
        print(" ".join(row))

    print()
