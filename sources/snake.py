import pygame

from pygame import Rect, Surface
from constants import GL_SNAKE_EYE_COLOUR, GL_SNAKE_HEAD_COLOUR, \
    GL_SNAKE_PUPIL_COLOUR
from sources.apple import Apple
from sources.apple_color import AppleColour
from sources.direction_enum import Direction


class Snake:
    def __init__(self,
                 spawn_x_pos: int,
                 spawn_y_pos: int,
                 cell_length_px: int) -> None:
        self.cell_length_px: int = cell_length_px
        self.segments: list[Rect] = [
            # Tail
            Rect((spawn_x_pos - cell_length_px, spawn_y_pos),
                 (cell_length_px, cell_length_px)),
            # Body
            Rect((spawn_x_pos, spawn_y_pos),
                 (cell_length_px, cell_length_px)),
            # Head
            Rect((spawn_x_pos + cell_length_px, spawn_y_pos),
                 (cell_length_px, cell_length_px))
        ]
        self.deltas: dict[Direction, tuple[int, int]] = {
            Direction.LEFT: (-self.cell_length_px, 0),
            Direction.RIGHT: (self.cell_length_px, 0),
            Direction.UP: (0, -self.cell_length_px),
            Direction.DOWN: (0, self.cell_length_px),
        }
        self._is_dead: bool = False
        self._head_surface: Surface = self._create_head_surface()

    def sim_next_move(self, direction: Direction) -> Rect:
        """Simulates the movement of the snake and returns the Rect object
        the head of the snake would use"""
        dx, dy = self.deltas[direction]
        return self.get_head().move(dx, dy)

    def move(self, next_snake_head: Rect, eaten_apple: Apple | None) -> None:
        """Each turn the snake obtains a new segment at its new head position
        and loses an element at its tail position, visually simulating its
        progress. Segment wise, this behaviour does +1 -1, which does not
        change the total length of the snake.

        When a green apple is eaten, prevents the snake from its default
        tail loss. Segment wise, only does +1, which increases the total length
        of the snake by one unit.

        When a red apple is eaten, applies a tail loss on top of the default
        one. Segment wise, does +1 -1 -1, which decreases the total length of
        the snake by one unit.
        """
        new_head: Rect = next_snake_head
        self.segments.append(new_head)

        # Green apple prevents the snake from its default shrinkage
        if eaten_apple and eaten_apple.colour == AppleColour.GREEN:
            return

        # Red apple leads to one extra tail loss
        if eaten_apple and eaten_apple.colour == AppleColour.RED:
            self._remove_tail()

        self._remove_tail()

    def get_head(self) -> Rect:
        return self.segments[-1]

    def get_head_pos(self) -> tuple[int, int]:
        head = self.get_head()
        return head.x, head.y

    def get_tail(self) -> Rect:
        return self.segments[0]

    def get_body_without_head(self) -> list[Rect]:
        return self.segments[:-1]

    def get_neck(self) -> Rect:
        return self.segments[-2]

    def _remove_tail(self) -> None:
        self.segments.pop(0)

        # If snake has no more segments, snake dies
        if len(self.segments) == 0:
            self.die()

    def is_dead(self) -> bool:
        return self._is_dead

    def die(self) -> None:
        self._is_dead = True

    def get_head_surface(self) -> Surface:
        return self._head_surface

    def _create_head_surface(self) -> Surface:
        # Creates the surface and the rectangle to draw on
        surface = Surface((self.cell_length_px, self.cell_length_px))
        rect = (0, 0, self.cell_length_px, self.cell_length_px)

        # Draws the rectangle (background) within the surface
        pygame.draw.rect(surface, GL_SNAKE_HEAD_COLOUR, rect)

        # Uses the length of the cell to define circles position and sizes
        eye_radius = self.cell_length_px // 4
        eye_offset = self.cell_length_px // 4
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
                           (self.cell_length_px - eye_offset, eye_offset),
                           eye_radius)
        pygame.draw.circle(surface, GL_SNAKE_PUPIL_COLOUR,
                           (self.cell_length_px - eye_offset, eye_offset),
                           pupil_radius)

        return surface
