import pygame

from pygame import Surface

from constants import CL_GRID_COLOUR, GL_BOARD_SIZE_IN_CELL


def create_grid_surface(cell_length_px: int) -> Surface:
    grid_length_px: int = GL_BOARD_SIZE_IN_CELL * cell_length_px

    grid: Surface = Surface(
        (grid_length_px + 1, grid_length_px + 1), pygame.SRCALPHA)

    for i in range(GL_BOARD_SIZE_IN_CELL + 1):
        pos = i * cell_length_px
        # Vertical
        pygame.draw.line(grid, CL_GRID_COLOUR, (pos, 0),
                         (pos, grid_length_px))
        # Horizontal
        pygame.draw.line(grid, CL_GRID_COLOUR, (0, pos),
                         (grid_length_px, pos))

    return grid
