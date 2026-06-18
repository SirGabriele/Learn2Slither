from sources.classes.apple import Apple
from sources.enums.colour_enum import Colour
from sources.enums.direction_enum import Direction
from sources.classes.snake_segments import SnakeSegments


class Snake:
    def __init__(self,
                 segments_indices: SnakeSegments) -> None:
        self._is_dead: bool = False
        self._segments: SnakeSegments = segments_indices
        self._eaten_apple: Apple | None = None
        self._deltas: dict[Direction, tuple[int, int]] = {
            Direction.UP: (-1, 0),
            Direction.RIGHT: (0, 1),
            Direction.DOWN: (1, 0),
            Direction.LEFT: (0, -1)
        }

    def sim_next_move(self, direction: Direction) -> tuple[int, int]:
        """Simulates the movement of the snake and returns indices it would
        have."""
        curr_row, curr_col = self._segments.head
        next_row, next_col = self._deltas[direction]
        return curr_row + next_row, curr_col + next_col

    def move(self, next_snake_head_coord: tuple[int, int]) -> None:
        """Each turn the snake obtains a new segment at its previous head
        position and loses an element at its tail position, visually
        simulating its progress. Segment wise, this behaviour does +1 -1, which
        does not change the total length of the snake.

        When a green apple is eaten, prevents the snake from its default
        tail loss. Segment wise, only does +1, which increases the total length
        of the snake by one unit.

        When a red apple is eaten, applies a tail loss on top of the default
        one. Segment wise, does +1 -1 -1, which decreases the total length of
        the snake by one unit.
        """
        body = self._segments.body_board_coords

        body.append(next_snake_head_coord)

        if (apple := self._eaten_apple) is not None:
            if apple.colour == Colour.GREEN:
                return
            else:
                body.pop(0)

        if body:
            body.pop(0)

        if not body:
            self.die()

    #########################################################
    # ################## PROPERTIES #########################
    #########################################################

    @property
    def segments(self) -> SnakeSegments:
        return self._segments

    @property
    def eaten_apple(self) -> Apple | None:
        return self._eaten_apple

    #########################################################
    # ################## PUBLIC METHODS #####################
    #########################################################

    def is_dead(self) -> bool:
        return self._is_dead

    def die(self) -> None:
        self._is_dead = True

    def eat_apple(self,
                  next_snake_head_coord: tuple[int, int],
                  apples: list[Apple]) -> None:
        for apple in apples:
            if next_snake_head_coord == apple.board_coord:
                self.set_eaten_apple(apple)
                break

    def set_eaten_apple(self, apple: Apple | None) -> None:
        self._eaten_apple = apple

    def digest_apple(self) -> None:
        if self._eaten_apple is not None:
            self.set_eaten_apple(None)
