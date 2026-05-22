from pygame import Rect
from sources.classes.apple import Apple
from sources.classes.board import Board
from sources.collision.is_snake_collision_self import is_snake_collision_self
from sources.collision.is_snake_out_of_bound import is_snake_out_of_bound
from sources.enums.direction_enum import Direction
from sources.utils.get_eaten_apple import get_eaten_apple


def handle_movement(board: Board, direction: Direction) -> Apple | None:
    snake = board.snake
    next_snake_head: Rect = snake.sim_next_move(direction)

    if is_snake_out_of_bound(board.rect, next_snake_head) or \
            is_snake_collision_self(next_snake_head, snake.segments):
        snake.die()
        return None

    eaten_apple: Apple | None = get_eaten_apple(
        next_snake_head,
        board.apples
    )

    snake.move(next_snake_head, eaten_apple)

    if eaten_apple:
        board.handle_apple_eaten(eaten_apple)

    return eaten_apple