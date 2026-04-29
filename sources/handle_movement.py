from pygame import Rect
from sources.apple import Apple
from sources.board import Board
from sources.collision.is_snake_collision_self import is_snake_collision_self
from sources.collision.is_snake_out_of_bound import is_snake_out_of_bound
from sources.direction_enum import Direction
from sources.get_eaten_apple import get_eaten_apple


def handle_movement(board: Board, direction: Direction) -> None:
    next_snake_pos: Rect = board.snake.sim_next_move(direction)

    if is_snake_out_of_bound(board.rect, next_snake_pos) or \
            is_snake_collision_self(next_snake_pos, board.snake.segments):
        board.snake.die()
        return

    eaten_apple: Apple | None = get_eaten_apple(
        next_snake_pos,
        board.apples
    )

    board.snake.move(next_snake_pos, eaten_apple)

    if eaten_apple:
        board.handle_apple_eaten(eaten_apple)
