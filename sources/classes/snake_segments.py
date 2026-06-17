from dataclasses import dataclass


@dataclass
class SnakeSegments:
    # In this list, the first element is the oldest, the closest to the tail.
    # The last element is the newest, the closest to the head.
    body_board_coords: list[tuple[int, int]]

    @property
    def head(self) -> tuple[int, int]:
        return self.body_board_coords[-1]

    @head.setter
    def head(self, value: tuple[int, int]) -> None:
        self.body_board_coords[-1] = value

    @property
    def tail(self) -> tuple[int, int] | None:
        return (self.body_board_coords[0]
                if len(self.body_board_coords) > 1
                else None)

    @property
    def middle(self) -> list[tuple[int, int]]:
        return (self.body_board_coords[1:-1]
                if len(self.body_board_coords) > 2
                else [])
