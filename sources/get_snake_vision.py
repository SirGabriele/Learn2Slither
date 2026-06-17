import numpy as np

from constants import GL_GAME_STATE_EMPTY
from sources.classes.board import Board


def get_snake_vision(board: Board) -> np.ndarray:
    """Returns a ndarray that contains a cross-like representing the
    snake's field of vision."""
    # Updates the playable area to have the current state of the game.
    board.update_playable_area()

    head_row, head_col = board.snake.segments.head

    # Creates a new ndarray of similar shape as playable area.
    cross_view = np.full(board.full_board.shape, GL_GAME_STATE_EMPTY,
                         dtype='<U1')

    # Copies the values on the snake's head row.
    cross_view[head_row + 1, :] = board.full_board[head_row + 1, :]

    # Copies the values on the snake's head column.
    cross_view[:, head_col + 1] = board.full_board[:, head_col + 1]

    return cross_view
