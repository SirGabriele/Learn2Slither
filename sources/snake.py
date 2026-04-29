from pygame import Rect

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

    def sim_next_move(self, direction: Direction) -> Rect:
        """Simulates the movement of the snake and returns the position in
        which the snake would then be"""
        dx, dy = self.deltas[direction]
        return self.get_head().move(dx, dy)

    def move(self, next_snake_pos: Rect, eaten_apple: Apple | None) -> None:
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
        new_head: Rect = next_snake_pos
        self.segments.append(new_head)

        # Green apple prevents the snake from its default shrinkage
        if eaten_apple and eaten_apple.colour == AppleColour.GREEN:
            # TODO gérer le cas où le serpent fait la taille max
            return

        # Red apple leads to one extra tail loss
        if eaten_apple and eaten_apple.colour == AppleColour.RED:
            self._remove_tail()

        self._remove_tail()

    def get_head(self) -> Rect:
        return self.segments[-1]

    def get_tail(self) -> Rect:
        return self.segments[0]

    def _remove_tail(self) -> None:
        self.segments.pop(0)

        # If snake has no more segments, snake dies
        if len(self.segments) == 0:
            self.die()

    def is_dead(self) -> bool:
        return self._is_dead

    def die(self) -> None:
        self._is_dead = True
