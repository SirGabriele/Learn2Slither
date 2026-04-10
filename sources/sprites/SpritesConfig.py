from constants import SPRITE_NAT_LENGTH
from enum import Enum


class SpriteName(Enum):
    """Enum containing all sprite names"""
    SNAKE_HEAD_UP = "snake_head_up"
    SNAKE_HEAD_DOWN = "snake_head_down"
    SNAKE_HEAD_LEFT = "snake_head_left"
    SNAKE_HEAD_RIGHT = "snake_head_right"
    SNAKE_BODY_STRAIGHT_VER = "snake_body_straight_ver"
    SNAKE_BODY_STRAIGHT_HOR = "snake_body_straight_hor"
    SNAKE_BODY_CORNER_TOP_LEFT = "snake_body_corner_top_left"
    SNAKE_BODY_CORNER_TOP_RIGHT = "snake_body_corner_top_right"
    SNAKE_BODY_CORNER_BOTTOM_LEFT = "snake_body_corner_bottom_left"
    SNAKE_BODY_CORNER_BOTTOM_RIGHT = "snake_body_corner_top_right"
    SNAKE_TAIL_UP = "snake_tail_up"
    SNAKE_TAIL_DOWN = "snake_tail_down"
    SNAKE_TAIL_LEFT = "snake_tail_left"
    SNAKE_TAIL_RIGHT = "snake_tail_right"
    APPLE_RED = "apple_red"
    APPLE_GREEN = "apple_green"


def coords_to_px(coords_idx: tuple[int, int]) -> tuple[int, int]:
    """Converts a tuple (idx_x, idx_y) of indices in the sprite sheet to a
    tuple (px_x, px_y) of their corresponding pixel coordinates"""
    return (
        SPRITE_NAT_LENGTH * coords_idx[0],
        SPRITE_NAT_LENGTH * coords_idx[1]
    )


SPRITES_NAME_TO_COORDS: dict[SpriteName, tuple[int, int]] = {
    SpriteName.SNAKE_HEAD_UP: coords_to_px((3, 0)),
    SpriteName.SNAKE_HEAD_DOWN: coords_to_px((4, 1)),
    SpriteName.SNAKE_HEAD_LEFT: coords_to_px((3, 1)),
    SpriteName.SNAKE_HEAD_RIGHT: coords_to_px((4, 0)),
    SpriteName.SNAKE_BODY_STRAIGHT_VER: coords_to_px((1, 1)),
    SpriteName.SNAKE_BODY_STRAIGHT_HOR: coords_to_px((1, 0)),
    SpriteName.SNAKE_BODY_CORNER_TOP_LEFT: coords_to_px((0, 0)),
    SpriteName.SNAKE_BODY_CORNER_TOP_RIGHT: coords_to_px((2, 0)),
    SpriteName.SNAKE_BODY_CORNER_BOTTOM_LEFT: coords_to_px((0, 1)),
    SpriteName.SNAKE_BODY_CORNER_BOTTOM_RIGHT: coords_to_px((2, 1)),
    SpriteName.SNAKE_TAIL_UP: coords_to_px((3, 2)),
    SpriteName.SNAKE_TAIL_DOWN: coords_to_px((4, 3)),
    SpriteName.SNAKE_TAIL_LEFT: coords_to_px((3, 3)),
    SpriteName.SNAKE_TAIL_RIGHT: coords_to_px((4, 2)),
    SpriteName.APPLE_RED: coords_to_px((0, 3)),
    SpriteName.APPLE_GREEN: coords_to_px((1, 3))
}
