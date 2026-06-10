import numpy as np

from pygame import Rect, Surface
from random import randrange, sample

from constants import CL_GRID_COLOUR, GL_BOARD_SIZE_IN_CELL, \
    GL_GAME_STATE_FREE_CELL, GL_GAME_STATE_GREEN_APPLE, \
    GL_GAME_STATE_RED_APPLE, GL_GAME_STATE_SNAKE_BODY, \
    GL_GAME_STATE_SNAKE_HEAD, GL_GAME_STATE_SNAKE_TAIL
from sources.classes.apple import Apple
from sources.classes.snake import Snake
from sources.classes.snake_segments import SnakeSegments
from sources.enums.colour_enum import Colour
from sources.utils.create_grid_surface import create_grid_surface
from sources.utils.fill_walls import fill_walls


class Board:
    def __init__(self,
                 win_width: int,
                 win_height: int,
                 cell_length_px: int) -> None:
        # board_center_w: float = (win_width / 2)
        # board_center_h: float = (win_height / 2)
        # board_size_in_px: int = GL_BOARD_SIZE_IN_CELL * cell_length_px
        # board_half_size_in_cell: int = GL_BOARD_SIZE_IN_CELL // 2
        # board_half_size_in_px: int = (
        #         board_half_size_in_cell * cell_length_px
        # )
        # l_border: int = int(board_center_w - board_half_size_in_px)
        # t_border: int = int(board_center_h - board_half_size_in_px)

        # self.half_size_in_px: int = board_half_size_in_px
        # self.size_in_cell: int = GL_BOARD_SIZE_IN_CELL
        # self.total_amount_of_cells = self.size_in_cell * self.size_in_cell
        # self.cell_length_px: int = cell_length_px
        # self.rect: Rect = pygame.Rect(
        #     l_border, t_border, board_size_in_px, board_size_in_px
        # )

        self._full_board = self._init_full_board()

        # Fills the board_array with walls
        fill_walls(self._full_board)

        # TODO tester les edge cases, crash a eu lieu
        snake_indices = self._init_snake_pos()
        self.snake: Snake = Snake(snake_indices)

        self._fill_snake()

        self._apples: list[Apple] | None = self._init_apples()

        self._fill_apples()

        # TODO ICI
        self._grid: Surface = create_grid_surface()
        self._game_win: bool = False

    # def generate_apple(self, colour: Colour) -> Apple | None:
    def generate_apples(self, colours: list[Colour]) -> list[Apple] | None:
        # Creates a ndarray[tuple] of all indices of the board that are free.
        free_indices = np.argwhere(self._full_board == GL_GAME_STATE_FREE_CELL)

        # TODO re-verifier ce cas
        if len(free_indices) == 0:
            self.win()
            return None

        free_indices = sample(free_indices.tolist(), len(colours))

        return [Apple(indices=indices, colour=colour) for indices, colour
                in zip(free_indices, colours)]

    def handle_apple_eaten(self, apple: Apple) -> None:
        # Remove the eaten apple from the list of apples
        self.apples.remove(apple)

        # Creates a new apple of the same colour
        if (apple := self.generate_apples(apple.colour)) is not None:
            self.apples.append(apple)

    def get_grid(self) -> Surface:
        return self._grid

    def is_win(self) -> bool:
        return self._game_win

    def win(self) -> None:
        self._game_win = True

    def get_full_board(self) -> np.ndarray:
        """Returns the whole board including the wall outline"""
        return self._full_board

    def _init_playable_area_view(self) -> np.ndarray:
        """Returns a view area without the wall outline."""
        return self._full_board[1:-1, 1:-1]

    def _init_snake_pos(self) -> SnakeSegments:
        # Selects a random cell on the grid that will correspond to the
        # snake's body.
        full_board_rows, full_board_cols = self._full_board.shape

        # In full board, index '0' and 'full_board_rows' are walls.
        # Thus, we start the range to 1 and stop it to full_board_rows - 1,
        # stop value being excluded
        body_row: int = randrange(1, full_board_rows - 1)
        body_col: int = randrange(1, full_board_cols - 1)

        # Maps out 4 adjacent cells.
        # Some could be out of bounds but since the body's index in is
        # bounds, there will always be at least 2 adjacent indices in bounds
        # as well.
        adjacent_cells: list[tuple[int, int]] = [
            (body_row - 1, body_col),  # Up
            (body_row, body_col + 1),  # Right
            (body_row + 1, body_col),  # Down
            (body_row, body_col - 1)  # Left
        ]

        # Filters out the out of bound indices.
        valid_adjacent_cells: list[tuple[int, int]] = [
            (row, col) for row, col in adjacent_cells
            if 1 <= row < full_board_rows - 1
               and 1 <= col < full_board_cols - 1
        ]

        head_indices, tail_indices = sample(valid_adjacent_cells, 2)
        body_indices = (body_row, body_col)

        return SnakeSegments(head_indices=head_indices,
                             body_indices=[body_indices],
                             tail_indices=tail_indices)

    def _fill_snake(self):
        segments = self.snake.get_segments()

        # Head.
        head_row, head_col = segments.head_indices
        self._full_board[head_row, head_col] = GL_GAME_STATE_SNAKE_HEAD

        # Body.
        for body_row, body_col in segments.body_indices:
            self._full_board[body_row, body_col] = GL_GAME_STATE_SNAKE_BODY

        # Tail.
        tail_row, tail_col = segments.tail_indices
        self._full_board[tail_row, tail_col] = GL_GAME_STATE_SNAKE_TAIL

    def _init_apples(self) -> list[Apple] | None:
        return self.generate_apples([Colour.GREEN, Colour.GREEN, Colour.RED])

    def _fill_apples(self):
        if self._apples is None:
            return

        for apple in self._apples:
            row, col = apple.indices

            if apple.colour == Colour.GREEN:
                self._full_board[row][col] = GL_GAME_STATE_GREEN_APPLE
            else:
                self._full_board[row][col] = GL_GAME_STATE_RED_APPLE

    def _init_full_board(self) -> np.ndarray:
        # Adds 2 to have walls on each edge
        board_size_in_cell_with_walls = GL_BOARD_SIZE_IN_CELL + 2
        board_shape: tuple[int, int] = (
            board_size_in_cell_with_walls, board_size_in_cell_with_walls
        )

        return np.full(board_shape, GL_GAME_STATE_FREE_CELL, dtype='<U1')
