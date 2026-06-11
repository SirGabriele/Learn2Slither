import numpy as np

from constants import GL_BOARD_SIZE_IN_CELL, GL_GAME_STATE_FREE_CELL


def init_full_board() -> np.ndarray:
    # Adds 2 to have walls on each edge
    board_size_in_cell_with_walls = GL_BOARD_SIZE_IN_CELL + 2
    board_shape: tuple[int, int] = (
        board_size_in_cell_with_walls, board_size_in_cell_with_walls
    )

    return np.full(board_shape, GL_GAME_STATE_FREE_CELL, dtype='<U1')
