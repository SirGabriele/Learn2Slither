import pygame

from constants import SPRITE_NAT_LENGTH, SPRITE_NAT_RESOLUTION, \
    PATH_SPRITE_SHEET
from pygame import Rect, Surface
from sources.sprites.SpritesConfig import SPRITES_NAME_TO_COORDS, SpriteName


class SpriteManager:
    def __init__(self, cell_length: int):
        self.sprite_sheet = (pygame.image.load(PATH_SPRITE_SHEET)
                             .convert_alpha())
        self._scale_factor = cell_length / SPRITE_NAT_LENGTH
        print(self._scale_factor)
        self._cache: dict[SpriteName, Surface] = {}

    def get(self, sprite_name: SpriteName) -> Surface:
        """Returns the Surface of the specified sprite. Throws ValueError
        if not found."""
        if sprite_name in self._cache:
            return self._cache[sprite_name]

        if sprite_name not in SPRITES_NAME_TO_COORDS:
            raise ValueError(f"Unknown sprite name: {sprite_name}")

        coords = SPRITES_NAME_TO_COORDS[sprite_name]
        sprite = self._extract(coords)

        scaled_sprite = pygame.transform.scale_by(sprite, self._scale_factor)

        self._cache[sprite_name] = scaled_sprite
        return scaled_sprite

    def _extract(self, coords: tuple[int, int]) -> Surface:
        """Returns the sprite at the provided coordinates."""
        rect: Rect = pygame.Rect(coords, SPRITE_NAT_RESOLUTION)
        sprite: Surface = pygame.Surface(rect.size, pygame.SRCALPHA)
        sprite.blit(self.sprite_sheet, (0, 0), rect)
        return sprite
