from sources.classes.apple import Apple
from sources.classes.board import Board
from sources.classes.snake import Snake
from sources.collision.is_snake_collision_self import is_snake_collision_self
from sources.collision.is_snake_out_of_bound import is_snake_out_of_bound
from sources.enums.direction_enum import Direction


def handle_movement(board: Board, direction: Direction) -> None:
    snake: Snake = board.snake
    apples: list[Apple] = board.apples

    # Gets the coordinates at which the snake's head would be after moving.
    next_snake_head_indices: tuple[int, int] = snake.sim_next_move(direction)

    if (is_snake_out_of_bound(board.playable_area,
                              next_snake_head_indices)
            or is_snake_collision_self(snake.segments.middle,
                                       next_snake_head_indices)):
        snake.die()
        return

    snake.eat_apple(
        next_snake_head_indices,
        apples
    )

    snake.move(next_snake_head_indices)

    if (snake.is_dead() is False
            and (apple := snake.eaten_apple) is not None):
        board.handle_apple_eaten(apple)
