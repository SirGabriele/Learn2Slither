from pygame import Rect
from sources.apple_color import AppleColour


class Apple:
    def __init__(self, rect: Rect, colour: AppleColour) -> None:
        self.rect: Rect = rect
        self.colour: AppleColour = colour
