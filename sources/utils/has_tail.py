from sources.classes.snake import Snake


def has_tail(snake: Snake) -> bool:
    return len(snake._segments) >= 2
