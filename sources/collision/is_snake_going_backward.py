from pygame import Rect
from sources.snake import Snake
from sources.utils.has_tail import has_tail


def is_snake_going_backward(next_snake_head: Rect, snake: Snake) -> bool:
    """Checks if the snake is going backward, colliding with its 'neck'"""
    if has_tail(snake):
        return next_snake_head.colliderect(snake.get_neck())
    return False
