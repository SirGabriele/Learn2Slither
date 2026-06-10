import numpy as np

from constants import GL_GAME_STATE_WALL


def fill_walls(board: np.ndarray):
    # Top row
    board[0, :] = GL_GAME_STATE_WALL
    # Bottom row
    board[-1, :] = GL_GAME_STATE_WALL
    # Left column
    board[:, 0] = GL_GAME_STATE_WALL
    # Right column
    board[:, -1] = GL_GAME_STATE_WALL
