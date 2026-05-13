import numpy as np

from constants import GL_VISION_EMPTY, GL_VISION_FREE_CELL, \
    GL_VISION_GREEN_APPLE, \
    GL_VISION_RED_APPLE, \
    GL_VISION_SNAKE_BODY, \
    GL_VISION_SNAKE_HEAD, \
    GL_VISION_SNAKE_TAIL, GL_VISION_WALL
from sources.board import Board
from sources.enums.colour_enum import Colour
from sources.utils.has_body import has_body
from sources.utils.has_tail import has_tail


def get_board_index(px_array: np.ndarray,
                    offset: int,
                    cell_length_px: int) -> np.ndarray:
    return (px_array - offset) // cell_length_px


def fill_wall(array: np.ndarray):
    # Top row
    array[0, :] = GL_VISION_WALL
    # Bottom row
    array[-1, :] = GL_VISION_WALL
    # Left column
    array[:, 0] = GL_VISION_WALL
    # Right column
    array[:, -1] = GL_VISION_WALL


def get_snake_layer(array: np.ndarray,
                    board: Board,
                    left_offset: int,
                    top_offset: int):
    lefts = np.array([s.left for s in board.snake.segments])
    tops = np.array([s.top for s in board.snake.segments])

    col_idxs = get_board_index(lefts, left_offset, board.cell_length_px)
    row_idxs = get_board_index(tops, top_offset, board.cell_length_px)

    array[row_idxs[-1] + 1, col_idxs[-1] + 1] = GL_VISION_SNAKE_HEAD
    if has_body(board.snake):
        array[row_idxs[1:-1] + 1, col_idxs[1:-1] + 1] = GL_VISION_SNAKE_BODY
    if has_tail(board.snake):
        array[row_idxs[0] + 1, col_idxs[0] + 1] = GL_VISION_SNAKE_TAIL


def get_apple_layer(array: np.ndarray,
                    board: Board,
                    apple_colour: Colour,
                    apple_symbol: str,
                    left_offset: int,
                    top_offset: int):
    lefts = np.array([a.rect.left for a in board.apples if
                      a.colour == apple_colour])
    tops = np.array([a.rect.top for a in board.apples if a.colour ==
                     apple_colour])

    col_idxs = get_board_index(lefts, left_offset, board.cell_length_px)
    row_idxs = get_board_index(tops, top_offset, board.cell_length_px)

    array[row_idxs + 1, col_idxs + 1] = apple_symbol


def scan_snake_vision(board: Board) -> np.ndarray:
    # Extracts the left and top pos of the board's rectangle
    left_offset, top_offset, _, _ = board.rect

    board_size_in_cell_with_walls = board.size_in_cell + 2
    board_shape: tuple[int, int] = (
        board_size_in_cell_with_walls, board_size_in_cell_with_walls
    )

    board_array = np.full(board_shape, GL_VISION_FREE_CELL, dtype='<U1')

    # Fills the array with wall symbols
    fill_wall(board_array)

    # Fills the array with snake symbols
    get_snake_layer(board_array, board, left_offset, top_offset)

    # Fills the array with green apple symbols
    get_apple_layer(board_array, board, Colour.GREEN,
                    GL_VISION_GREEN_APPLE,
                    left_offset, top_offset)

    # Fills the array with red apple symbols
    get_apple_layer(board_array, board, Colour.RED,
                    GL_VISION_RED_APPLE,
                    left_offset, top_offset)

    # Finds the coordinates of the snake's head
    head_coords = np.where(board_array == GL_VISION_SNAKE_HEAD)
    head_row, head_col = head_coords[0][0], head_coords[1][0]

    # Creates a mask of True values
    mask = np.ones(board_array.shape, dtype=bool)

    # Sets the head's row and column to False so they do not get erased
    mask[head_row, :] = False
    mask[:, head_col] = False

    # Erases every True values of the array
    board_array[mask] = GL_VISION_EMPTY

    return board_array
