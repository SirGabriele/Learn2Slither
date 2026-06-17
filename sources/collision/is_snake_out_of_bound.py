import numpy as np


def is_snake_out_of_bound(playable_area: np.ndarray,
                          next_snake_head_coord: tuple[int, int]) -> bool:
    """Checks if the snake is out of the board's boundaries."""
    playable_area_rows, playable_area_cols = playable_area.shape
    col, row = next_snake_head_coord
    return (False if (0 <= row < playable_area_rows
                      and 0 <= col < playable_area_cols)
            else True)
