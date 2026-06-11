def get_window_dimensions(nb_cells: int) -> tuple[int, int, int]:
    """Given a number of cells, determines the window's pixel size and the
    size each cell should measure. The number of cells must be between 5 and
    30"""

    if nb_cells <= 4:
        raise ValueError("Board size should be more than 5 cells")

    # Example : for 10 cells, creates a 1024px/728px window and each cell is
    # 64px.
    configs = {
        10: (1024, 728, 64),
        15: (1024, 728, 40),
        20: (1366, 768, 32),
        30: (1366, 768, 24),
    }

    for limit, config in configs.items():
        if nb_cells <= limit:
            return config

    raise ValueError("Board size should be less than 30 cells")
