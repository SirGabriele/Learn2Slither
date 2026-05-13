import pygame

from pygame import Rect, Surface
from constants import GL_BOARD_BG_COLOUR, GL_SNAKE_BODY_COLOUR, \
    GL_SNAKE_TAIL_COLOUR
from sources.classes.apple import Apple
from sources.classes.board import Board
from sources.classes.snake import Snake
from sources.utils.has_body import has_body
from sources.utils.has_tail import has_tail


def draw_grid(surface: Surface, grid: Surface, pos: tuple[int, int]):
    surface.blit(grid, pos)


def draw_head(surface: Surface, head: Surface, pos: tuple[int, int]):
    surface.blit(head, pos)


def draw_tail(surface: Surface, tail: Rect):
    pygame.draw.rect(surface, GL_SNAKE_TAIL_COLOUR, tail)


def draw_snake(surface: Surface, snake: Snake):
    draw_head(surface, snake.get_head_surface(), snake.get_head_pos())

    if has_body(snake):
        for segment in snake.get_body():
            pygame.draw.rect(surface, GL_SNAKE_BODY_COLOUR, segment)

    if has_tail(snake):
        draw_tail(surface, snake.get_tail())


def draw_apples(surface: Surface, apples: list[Apple]):
    for apple in apples:
        pygame.draw.rect(surface, apple.colour.value, apple.rect)


def draw_game(surface: Surface, board: Board):
    surface.fill(GL_BOARD_BG_COLOUR)

    # Draw snake
    draw_snake(surface, board.snake)

    # Draw apples
    draw_apples(surface, board.apples)

    # Draw grid at the end to keep it on the foreground
    draw_grid(surface, board.get_grid(), (board.rect.left, board.rect.top))
