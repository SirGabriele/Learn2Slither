from dataclasses import dataclass


@dataclass
class SnakeSegments:
    head_board_coord: tuple[int, int]
    body_board_coords: list[tuple[int, int]] | None
    tail_board_coord: tuple[int, int] | None
