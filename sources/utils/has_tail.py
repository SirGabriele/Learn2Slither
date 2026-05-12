from sources.snake import Snake


def has_tail(snake: Snake) -> bool:
    return len(snake.segments) >= 2
