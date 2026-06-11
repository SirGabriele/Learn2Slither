import numpy as np

from random import randrange, sample

from constants import GL_GAME_STATE_FREE_CELL, GL_GAME_STATE_GREEN_APPLE, \
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

        # Only contains the playable area.
        self._playable_area: np.ndarray = self._init_playable_area_view()

        # Fills the board_array with walls.
        fill_walls(self._full_board)

        snake_indices = self._init_snake_pos()
        self._snake: Snake = Snake(snake_indices)
        self._fill_snake()

        self._apples: list[Apple] | None = self._init_apples()
        if self._apples is None:
            raise InitialisationException("self._apples")
        self.fill_apples(self._apples)

        self._game_win: bool = False

    def generate_apples(self, colours: list[Colour]) -> list[Apple] | None:
        # Creates a ndarray[tuple] of all indices of the board that are free.
        free_indices = np.argwhere(
            self._playable_area == GL_GAME_STATE_FREE_CELL)

        # TODO re-verifier ce cas
        if len(free_indices) == 0:
            self.win()
            return None

        free_indices = sample(free_indices.tolist(), len(colours))

        return [Apple(board_coord=indices, colour=colour) for indices, colour
                in zip(free_indices, colours)]

    # def handle_apple_eaten(self, apple: Apple) -> None:
    #     # Remove the eaten apple from the list of apples
    #     self.apples.remove(apple)
    #
    #     # Creates a new apple of the same colour
    #     if (apple := self.generate_apples(apple.colour)) is not None:
    #         self.apples.append(apple)

    def is_win(self) -> bool:
        return self._game_win

    def win(self) -> None:
        self._game_win = True

    def get_full_board(self) -> np.ndarray:
        return self._full_board

    def get_snake(self) -> Snake:
        return self._snake

    def get_apples(self) -> list[Apple] | None:
        return self._apples

    def _init_playable_area_view(self) -> np.ndarray:
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

        return SnakeSegments(head_board_coord=head_indices,
                             body_board_coords=[body_indices],
                             tail_board_coord=tail_indices)

    def _fill_snake(self):
        segments = self._snake.get_segments()

        # Head.
        head_row, head_col = segments.head_board_coord
        self._playable_area[head_row, head_col] = GL_GAME_STATE_SNAKE_HEAD

        # Body.
        if self._snake.get_segments().body_board_coords is not None:
            for body_row, body_col in segments.body_board_coords:
                self._playable_area[
                    body_row, body_col] = GL_GAME_STATE_SNAKE_BODY

        # Tail.
        if self._snake.get_segments().tail_board_coord is not None:
            tail_row, tail_col = segments.tail_board_coord
            self._playable_area[tail_row, tail_col] = GL_GAME_STATE_SNAKE_TAIL

    def _init_apples(self) -> list[Apple] | None:
        return self.generate_apples([Colour.GREEN, Colour.GREEN, Colour.RED])

    def fill_apples(self, apples: list[Apple]):
        if apples is None:
            return

        for apple in apples:
            row, col = apple.board_coord

            if apple.colour == Colour.GREEN:
                self._playable_area[row][col] = GL_GAME_STATE_GREEN_APPLE
            else:
                self._playable_area[row][col] = GL_GAME_STATE_RED_APPLE
