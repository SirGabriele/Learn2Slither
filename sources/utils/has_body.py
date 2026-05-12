from sources.snake import Snake


def has_body(snake: Snake) -> bool:
    return len(snake.segments) >= 3
