from pygame import Rect
from sources.apple import Apple


def get_eaten_apple(snake_head: Rect, apples: list[Apple]) -> Apple | None:
    """Returns the apple if it collides with the snake. None otherwise."""
    return next(
        (apple for apple in apples if snake_head.colliderect(apple)),
        None
    )
