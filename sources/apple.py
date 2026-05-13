from pygame import Rect
from sources.enums.colour_enum import Colour


class Apple:
    def __init__(self, rect: Rect, colour: Colour) -> None:
        self.rect: Rect = rect
        self.colour: Colour = colour
