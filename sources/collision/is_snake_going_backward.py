from pygame import Rect
from sources.snake import Snake


def is_snake_going_backward(next_snake_head: Rect, snake: Snake) -> bool:
    """Checks if the snake is going backward, colliding with its 'neck'"""
    return next_snake_head.colliderect(snake.get_neck())
