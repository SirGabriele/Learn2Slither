import pygame

from pygame import Clock, Rect, Surface

from constants import GL_BOARD_BG_COLOUR, GL_BOARD_SIZE_IN_CELL, \
    GL_FRAME_PER_SECOND, GL_SNAKE_BODY_COLOUR, GL_SNAKE_TAIL_COLOUR

from sources.classes.apple import Apple
from sources.classes.snake import Snake
from sources.utils.board_coord_to_window_coord import (
    board_coord_to_window_coord)
from sources.utils.create_grid_surface import create_grid_surface
from sources.utils.create_head_surface import create_head_surface


class Renderer:
    def __init__(self,
                 visual_mode: bool,
                 window_dimensions: tuple[int, int, int]) -> None:
        win_width, win_height, cell_length_px = window_dimensions

        self._cell_length_px = cell_length_px

        board_center_w: float = (win_width / 2)
        board_center_h: float = (win_height / 2)

        board_half_size_in_cell: int = GL_BOARD_SIZE_IN_CELL // 2
        board_half_size_in_px: int = (
                board_half_size_in_cell * self._cell_length_px
        )

        self._left_offset: int = int(board_center_w - board_half_size_in_px)
        self._top_offset: int = int(board_center_h - board_half_size_in_px)

        self._grid: Surface = create_grid_surface(self._cell_length_px)

        # Creates a Surface with the window's dimensions
        self._surface: Surface = pygame.display.set_mode(
            (win_width, win_height))

        self._visual_mode: bool = visual_mode

        # Creates a Clock object that is used to refresh the screen a limited
        # amount of times per second
        self._clock: Clock = Clock()

        self._snake_head_surface: Surface = create_head_surface(
            self._cell_length_px)

    def update(self,
               snake: Snake,
               apples: list[Apple] | None,
               tick: bool = False) -> None:
        self._draw_game(snake, apples)

        pygame.display.update()

        if tick:
            self._tick()

    def _tick(self) -> None:
        self._clock.tick(GL_FRAME_PER_SECOND)

    def _draw_game(self, snake: Snake, apples: list[Apple] | None):
        self._surface.fill(GL_BOARD_BG_COLOUR)

        # Draws snake
        self._draw_snake(snake)

        if apples is not None:
            # Draws apples
            self._draw_apples(apples)

        # Draws grid at the end to keep it on the foreground
        self._draw_grid()

    def _draw_grid(self) -> None:
        self._surface.blit(self._grid, (self._left_offset, self._top_offset))

    def _draw_apples(self, apples: list[Apple]) -> None:
        for apple in apples:
            # Creates a Rect at window coord (0, 0)
            apple_rect: Rect = Rect(0, 0, self._cell_length_px,
                                    self._cell_length_px)

            # Moves Rect to appropriate window coord
            apple_rect.topleft = board_coord_to_window_coord(
                self._left_offset,
                self._top_offset,
                self._cell_length_px,
                apple.board_coord
            )

            # Draws on the surface
            pygame.draw.rect(self._surface, apple.colour.value,
                             apple_rect)

    def _draw_snake(self, snake: Snake) -> None:
        self._draw_head(snake.get_segments().head_board_coord)

        if snake.get_segments().body_board_coords is not None:
            self._draw_body(snake.get_segments().body_board_coords)

        if snake.get_segments().tail_board_coord is not None:
            self._draw_tail(snake.get_segments().tail_board_coord)

    def _draw_head(self, head_board_coord: tuple[int, int]) -> None:
        snake_window_coord = board_coord_to_window_coord(
            self._left_offset,
            self._top_offset,
            self._cell_length_px,
            head_board_coord
        )

        # Puts the snake head Surface on the main game Surface at appropriate
        # coord
        self._surface.blit(self._snake_head_surface, snake_window_coord)

    def _draw_body(self, body_board_coords: list[tuple[int, int]]) -> None:
        for board_coord in body_board_coords:
            # Creates a Rect at window coord (0, 0)
            body_rect: Rect = Rect(0, 0, self._cell_length_px,
                                   self._cell_length_px)

            # Moves Rect to appropriate window coord
            body_rect.topleft = board_coord_to_window_coord(
                self._left_offset,
                self._top_offset,
                self._cell_length_px,
                board_coord
            )

            # Draws on the surface
            pygame.draw.rect(self._surface, GL_SNAKE_BODY_COLOUR,
                             body_rect)

    def _draw_tail(self, tail_board_coord: tuple[int, int]) -> None:
        # Creates a Rect at window coord (0, 0)
        tail_rect: Rect = Rect(0, 0, self._cell_length_px,
                               self._cell_length_px)

        # Moves Rect to appropriate window coord
        tail_rect.topleft = board_coord_to_window_coord(
            self._left_offset,
            self._top_offset,
            self._cell_length_px,
            tail_board_coord
        )

        # Draws on the surface
        pygame.draw.rect(self._surface, GL_SNAKE_TAIL_COLOUR, tail_rect)
