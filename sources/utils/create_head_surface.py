import pygame

from pygame import Surface

from constants import GL_SNAKE_EYE_COLOUR, GL_SNAKE_HEAD_COLOUR, \
    GL_SNAKE_PUPIL_COLOUR


def create_head_surface(cell_length_px: int) -> Surface:
    # Creates the surface and the rectangle to draw on
    surface = Surface((cell_length_px, cell_length_px))
    rect = (0, 0, cell_length_px, cell_length_px)

    # Draws the rectangle (background) within the surface
    pygame.draw.rect(surface, GL_SNAKE_HEAD_COLOUR, rect)

    # Uses the length of the cell to define circles position and sizes
    eye_radius = cell_length_px // 4
    eye_offset = cell_length_px // 4
    pupil_radius = eye_radius // 2

    # Draws left eye within the surface
    pygame.draw.circle(surface, GL_SNAKE_EYE_COLOUR,
                       (eye_offset, eye_offset),
                       eye_radius)
    pygame.draw.circle(surface, GL_SNAKE_PUPIL_COLOUR,
                       (eye_offset, eye_offset),
                       pupil_radius)

    # Draws right eye within the surface
    pygame.draw.circle(surface, GL_SNAKE_EYE_COLOUR,
                       (cell_length_px - eye_offset, eye_offset),
                       eye_radius)
    pygame.draw.circle(surface, GL_SNAKE_PUPIL_COLOUR,
                       (cell_length_px - eye_offset, eye_offset),
                       pupil_radius)

    return surface
