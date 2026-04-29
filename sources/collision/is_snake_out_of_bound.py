from pygame import Rect


def is_snake_out_of_bound(rect: Rect, snake_pos: Rect) -> bool:
    """Checks if the snake is out of the bounds of the board"""
    # If simulated next snake position does not collide with the board's rect,
    # it means the snake has gone out of it
    return not rect.colliderect(snake_pos)
