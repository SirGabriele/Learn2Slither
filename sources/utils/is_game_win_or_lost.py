from sources.classes.board import Board


def is_game_win_or_lost(board: Board) -> bool:
    return board.is_win() or board.snake.is_dead()
