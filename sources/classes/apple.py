from dataclasses import dataclass

from sources.enums.colour_enum import Colour


@dataclass
class Apple:
    indices: tuple[int, int]
    colour: Colour
