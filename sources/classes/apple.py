from dataclasses import dataclass

from sources.enums.colour_enum import Colour


@dataclass
class Apple:
    board_coord: tuple[int, int]
    colour: Colour
