def get_window_size(nb_cells: int) -> tuple[tuple[int, int], int]:
    """Given a number of cells, determines the window's pixel size and the
    size each cell should measure"""
    if nb_cells <= 4:
        raise ValueError("Board size should be more than 5 cells")
    # For 10 cells, creates a 1024px/728px window and each cell is 64px
    elif nb_cells <= 10:
        return (1024, 728), 64
    elif nb_cells <= 15:
        return (1024, 728), 40
    elif nb_cells <= 20:
        return (1366, 768), 32
    elif nb_cells <= 30:
        return (1366, 768), 24
    else:
        raise ValueError("Board size should be less than 30 cells")
