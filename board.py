from constants import BOARD_SIZE_IN_CELL


class Board:
    def __init__(self, win_width: int, win_height: int, cell_length_px: int):
        board_center_w: float = (win_width / 2)
        board_center_h: float = (win_height / 2)
        board_size_in_px: int = BOARD_SIZE_IN_CELL * cell_length_px
        board_half_size_in_cell: float = BOARD_SIZE_IN_CELL / 2
        board_half_size_in_px: float = (
                board_half_size_in_cell * cell_length_px
        )

        self.size_in_px: int = board_size_in_px
        self.size_in_cell: int = BOARD_SIZE_IN_CELL
        self.cell_length_px: int = cell_length_px
        self.r_border: int = int(board_center_w + board_half_size_in_px)
        self.l_border: int = int(board_center_w - board_half_size_in_px)
        self.t_border: int = int(board_center_h - board_half_size_in_px)
        self.b_border: int = int(board_center_h + board_half_size_in_px)

    def __str__(self):
        return (
            f"Board: ('l={self.l_border}', 't={self.t_border}', "
            f"'r={self.r_border}', 'b={self.b_border}', "
            f"'size_in_px={self.size_in_px}', "
            f"'size_in_cell={self.size_in_cell}')"
        )
