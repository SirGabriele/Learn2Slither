from pygame import Rect


def is_snake_collision_self(snake_pos: Rect, segments: list[Rect]) -> bool:
    """Checks if the snake collides with any segment of its own body"""
    return any(snake_pos.colliderect(segment) for segment in segments)
