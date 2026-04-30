from pygame import Rect
from sources.apple import Apple
from sources.board import Board
from sources.collision.is_snake_collision_self import is_snake_collision_self
from sources.collision.is_snake_going_backward import is_snake_going_backward
from sources.collision.is_snake_out_of_bound import is_snake_out_of_bound
from sources.direction_enum import Direction
from sources.get_eaten_apple import get_eaten_apple


def handle_movement(board: Board, direction: Direction) -> None:
    snake = board.snake
    next_snake_head: Rect = snake.sim_next_move(direction)

    # Prevents snake from going backward
    if is_snake_going_backward(next_snake_head, snake):
        return

    if is_snake_out_of_bound(board.rect, next_snake_head) or \
            is_snake_collision_self(next_snake_head, snake.segments):
        snake.die()
        return

    eaten_apple: Apple | None = get_eaten_apple(
        next_snake_head,
        board.apples
    )

    snake.move(next_snake_head, eaten_apple)

    if eaten_apple:
        board.handle_apple_eaten(eaten_apple)
