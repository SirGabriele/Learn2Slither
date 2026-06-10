from dataclasses import dataclass


@dataclass
class SnakeSegments:
    head_indices: tuple[int, int]
    body_indices: list[tuple[int, int]]
    tail_indices: tuple[int, int]