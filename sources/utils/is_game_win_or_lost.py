from constants import GL_MAX_STEP
from sources.classes.board import Board


def is_game_win_or_lost(board: Board,
                        step_limit: int,
                        debug_mode: bool) -> bool:
    result: list[tuple[bool, str]] = [
        (board.is_win(), "You won!"),
        (board.snake.is_dead(), "You died!"),
        (step_limit >= GL_MAX_STEP, "Going in circles!"),
    ]

    for condition, msg in result:
        if condition:
            if debug_mode:
                print(msg)
            return True
    return False
