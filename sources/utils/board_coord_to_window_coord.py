def board_coord_to_window_coord(left_offset: int,
                                top_offset: int,
                                cell_length_px: int,
                                board_coord: tuple[int, int]) \
        -> tuple[int, int]:
    # Board coordinates are (row, col) but window wise they are (left, right).
    # Thus, we must calculate the window left offset using board col index and
    # window top offset using board row index.
    left = left_offset + (cell_length_px * board_coord[1])
    top = top_offset + (cell_length_px * board_coord[0])
    return left, top
