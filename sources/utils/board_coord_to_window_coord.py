def board_coord_to_window_coord(left_offset: int,
                                top_offset: int,
                                cell_length_px: int,
                                board_coord: tuple[int, int]) \
        -> tuple[int, int]:
    left = left_offset + (cell_length_px * board_coord[0])
    top = top_offset + (cell_length_px * board_coord[1])
    return left, top
