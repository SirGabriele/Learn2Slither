from pygame import Rect


def is_snake_collision_self(snake_pos: Rect, segments: list[Rect]) -> bool:
    """Checks if the snake collides with any segment of its own body apart
    from its tail (segments[0]). We do not check collision with the tail
    for the tail moves exactly as the head moves, which makes them
    impossible to collide."""
    return any(snake_pos.colliderect(segment) for segment in segments[1:])
