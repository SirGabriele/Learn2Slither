from constants import GL_MAX_STEP
from sources.classes.board import Board


def is_game_win_or_lost(board: Board, step_limit: int) -> bool:
    return board.is_win() or board._snake.is_dead() or step_limit >= GL_MAX_STEP
