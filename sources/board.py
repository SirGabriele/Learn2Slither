import pygame

from pygame import Rect, Surface
from random import randrange
from constants import CL_GRID_COLOUR, GL_BOARD_SIZE_IN_CELL
from sources.snake import Snake
from sources.apple import Apple
from sources.apple_color import AppleColour


class Board:
    def __init__(self,
                 win_width: int,
                 win_height: int,
                 cell_length_px: int) -> None:
        board_center_w: float = (win_width / 2)
        board_center_h: float = (win_height / 2)
        board_size_in_px: int = GL_BOARD_SIZE_IN_CELL * cell_length_px
        board_half_size_in_cell: int = GL_BOARD_SIZE_IN_CELL // 2
        board_half_size_in_px: int = (
                board_half_size_in_cell * cell_length_px
        )
        l_border: int = int(board_center_w - board_half_size_in_px)
        t_border: int = int(board_center_h - board_half_size_in_px)

        self.half_size_in_px: int = board_half_size_in_px
        self.size_in_cell: int = GL_BOARD_SIZE_IN_CELL
        self.total_amount_of_cells = self.size_in_cell * self.size_in_cell
        self.cell_length_px: int = cell_length_px
        self.rect: Rect = pygame.Rect(
            l_border, t_border, board_size_in_px, board_size_in_px
        )

        # Creates snake
        spawn_x_pos: int = self.rect.left + self.half_size_in_px
        spawn_y_pos: int = self.rect.top + self.half_size_in_px
        self.snake: Snake = Snake(spawn_x_pos, spawn_y_pos,
                                  self.cell_length_px)

        self.apples: list[Apple] = []
        if (apple := self.generate_apple(AppleColour.GREEN)) is not None:
            self.apples.append(apple)
        if (apple := self.generate_apple(AppleColour.GREEN)) is not None:
            self.apples.append(apple)
        if (apple := self.generate_apple(AppleColour.RED)) is not None:
            self.apples.append(apple)

        self._grid: Surface = self._create_grid_surface()
        self._game_win: bool = False

    def generate_apple(self, colour: AppleColour) -> Apple | None:
        # Creates a set containing all cells on which an obstacle is, including
        # snake segments and apples
        occupied_cells: set[tuple[int, int]] = (
                {(seg.x, seg.y) for seg in self.snake.segments} |
                {(apple.rect.x, apple.rect.y) for apple in self.apples}
        )
        # Adds + 1 because the apple that is currently being generated has not
        # been pushed in the apple list yet
        if len(occupied_cells) + 1 == self.total_amount_of_cells:
            self.win()
            return None

        while True:
            col: int = randrange(GL_BOARD_SIZE_IN_CELL)
            row: int = randrange(GL_BOARD_SIZE_IN_CELL)

            x: int = (col * self.cell_length_px) + self.rect.left
            y: int = (row * self.cell_length_px) + self.rect.top

            # Only leaves the loop when a free cell has been found
            if (occupied_cells is None or
                    (x, y) not in occupied_cells):
                # Add apple position to occupied cells
                return Apple(
                    Rect((x, y), (self.cell_length_px, self.cell_length_px)),
                    colour
                )

    def handle_apple_eaten(self, apple: Apple) -> None:
        # Remove the eaten apple from the list of apples
        self.apples.remove(apple)

        # Creates a new apple of the same colour
        if (apple := self.generate_apple(apple.colour)) is not None:
            self.apples.append(apple)

    def _create_grid_surface(self) -> Surface:
        grid_length_px: int = self.size_in_cell * self.cell_length_px

        grid: Surface = Surface(
            (grid_length_px + 1, grid_length_px + 1), pygame.SRCALPHA)

        for i in range(self.size_in_cell + 1):
            pos = i * self.cell_length_px
            # Vertical
            pygame.draw.line(grid, CL_GRID_COLOUR, (pos, 0),
                             (pos, grid_length_px))
            # Horizontal
            pygame.draw.line(grid, CL_GRID_COLOUR, (0, pos),
                             (grid_length_px, pos))

        return grid

    def get_grid(self) -> Surface:
        return self._grid

    def is_win(self) -> bool:
        return self._game_win

    def win(self) -> None:
        self._game_win = True
