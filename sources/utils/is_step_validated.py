import pygame

from pygame import Event


def is_step_validated(event: Event):
    if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
        return True
    return False
