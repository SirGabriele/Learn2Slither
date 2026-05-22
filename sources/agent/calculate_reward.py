from constants import GL_REWARD_DEATH, GL_REWARD_EMPTY_SPACE, \
    GL_REWARD_GREEN_APPLE, \
    GL_REWARD_RED_APPLE

from sources.classes.apple import Apple
from sources.enums.colour_enum import Colour


def calculate_reward(is_dead: bool,
                     eaten_apple: Apple | None) -> float:
    if is_dead:
        return GL_REWARD_DEATH

    if eaten_apple is not None:
        if eaten_apple.colour == Colour.GREEN:
            return GL_REWARD_GREEN_APPLE
        if eaten_apple.colour == Colour.RED:
            return GL_REWARD_RED_APPLE

    return GL_REWARD_EMPTY_SPACE