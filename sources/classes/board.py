import numpy as np

from random import randrange, sample

from constants import GL_BOARD_SIZE_IN_CELL, GL_GAME_STATE_FREE_CELL, \
    GL_GAME_STATE_GREEN_APPLE, \
    GL_GAME_STATE_RED_APPLE, GL_GAME_STATE_SNAKE_BODY, \
    GL_GAME_STATE_SNAKE_HEAD, GL_GAME_STATE_SNAKE_TAIL
from sources.classes.apple import Apple
from sources.classes.snake import Snake
from sources.classes.snake_segments import SnakeSegments
from sources.enums.colour_enum import Colour
from sources.exceptions.initialisation_exception import InitialisationException
from sources.utils.init_full_board import init_full_board
from sources.utils.fill_walls import fill_walls


class Board:
    def __init__(self) -> None:
        # Contains the wall outline.
        self._full_board: np.ndarray = init_full_board()

        # A view of full board that only contains the playable area.
        self._playable_area: np.ndarray = self._init_playable_area_view()

        # Fills the board_array with walls.
        fill_walls(self._full_board)

        snake_indices = self._init_snake_pos()
        self._snake: Snake = Snake(snake_indices)

        self._fill_snake()

        self._apples: list[Apple] = self._init_apples()
        if len(self._apples) == 0:
            raise InitialisationException("self._apples")

        self._fill_apples(self._apples)

        self._game_win: bool = False
        self._total_amount_cells = (GL_BOARD_SIZE_IN_CELL *
                                    GL_BOARD_SIZE_IN_CELL)

    #########################################################
    # ################## PROPERTIES #########################
    #########################################################

    @property
    def full_board(self) -> np.ndarray:
        return self._full_board

    @property
    def playable_area(self) -> np.ndarray:
        return self._playable_area

    @property
    def snake(self) -> Snake:
        return self._snake

    @property
    def apples(self) -> list[Apple]:
        return self._apples

    #########################################################
    # ################## PRIVATE METHODS ####################
    #########################################################

    def _init_playable_area_view(self) -> np.ndarray:
        """Returns a view of full board that does not contain the wall
        outline."""
        return self._full_board[1:-1, 1:-1]

    def _init_snake_pos(self) -> SnakeSegments:
        playable_area_rows, playable_area_cols = self._playable_area.shape

        # Selects a random cell on the grid that will correspond to the
        # snake's body.
        body_row: int = randrange(0, playable_area_rows - 1)
        body_col: int = randrange(0, playable_area_cols - 1)

        # Maps out 4 adjacent cells.
        # Some could be out of bounds but since the body's index in is
        # bounds. Since body can not be out of bound, there will always be at
        # least 2 adjacent indices in bounds.
        adjacent_cells: list[tuple[int, int]] = [
            (body_row - 1, body_col),  # Up
            (body_row, body_col + 1),  # Right
            (body_row + 1, body_col),  # Down
            (body_row, body_col - 1)  # Left
        ]

        # Filters out the out of bound indices.
        valid_adjacent_cells: list[tuple[int, int]] = [
            (row, col) for row, col in adjacent_cells
            if (0 <= row < playable_area_rows
                and 0 <= col < playable_area_cols)
        ]

        head_indices, tail_indices = sample(valid_adjacent_cells, 2)
        body_indices = (body_row, body_col)

        return SnakeSegments(
            body_board_coords=[tail_indices, body_indices, head_indices])

    def _init_apples(self) -> list[Apple]:
        return self.generate_apples(
            [Colour.GREEN, Colour.GREEN, Colour.RED],
            is_first_generation=True
        )

    def _fill_snake(self) -> None:
        """Updates the content of the playable area with the coordinates
        of all snake segments currently on the board."""
        segments = self._snake.segments

        # Head.
        head_row, head_col = segments.head
        self._playable_area[head_row, head_col] = GL_GAME_STATE_SNAKE_HEAD

        # Body.
        if len(self._snake.segments.middle) != 0:
            for body_row, body_col in segments.middle:
                self._playable_area[
                    body_row, body_col] = GL_GAME_STATE_SNAKE_BODY

        # Tail.
        if self._snake.segments.tail is not None:
            tail_row, tail_col = segments.tail
            self._playable_area[tail_row, tail_col] = GL_GAME_STATE_SNAKE_TAIL

    def _fill_apples(self, apples: list[Apple]) -> None:
        """Updates the content of the playable area with the coordinates
        of all apples currently on the board."""
        if apples is None:
            return

        for apple in apples:
            row, col = apple.board_coord

            if apple.colour == Colour.GREEN:
                self._playable_area[row][col] = GL_GAME_STATE_GREEN_APPLE
            else:
                self._playable_area[row][col] = GL_GAME_STATE_RED_APPLE

    #########################################################
    # ################## PUBLIC METHODS #####################
    #########################################################

    def generate_apples(self, colours: list[Colour],
                        is_first_generation: bool = False) -> list[Apple]:
        # Creates a ndarray[tuple] of all indices of the board that are free.
        free_indices = np.argwhere(
            self._playable_area == GL_GAME_STATE_FREE_CELL)

        if len(free_indices) == 0:
            # Only verifies winning condition once the initial generation
            # has been performed.
            if not is_first_generation:
                if not np.any(self._playable_area ==
                              GL_GAME_STATE_GREEN_APPLE):
                    self.win()
            return []

        free_indices = [
            (row, col)
            for row, col in sample(free_indices.tolist(), len(colours))
        ]

        return [Apple(board_coord=indices, colour=colour) for indices, colour
                in zip(free_indices, colours)]

    def handle_apple_eaten(self, apple: Apple) -> None:
        # Removes the eaten apple from the list of apples.
        self._apples.remove(apple)

        self.update_playable_area()

        # Creates a new apple of the same colour.
        apples = self.generate_apples([apple.colour])
        if len(apples) != 0:
            self._apples.append(apples[0])

    def is_win(self) -> bool:
        return self._game_win

    def win(self) -> None:
        self._game_win = True

    def update_playable_area(self) -> None:
        """Updates the content of the playable area with the coordinates
        of all snake segments and apples currently on the board."""
        self._playable_area[:] = GL_GAME_STATE_FREE_CELL
        self._fill_snake()
        self._fill_apples(self._apples)
