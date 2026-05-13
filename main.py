import pygame

from constants import GL_BOARD_SIZE_IN_CELL, GL_WINDOW_NAME
from pygame import Clock, Surface

from sources.board import Board
from sources.enums.direction_enum import Direction
from sources.draw_game import draw_game
from sources.handle_movement import handle_movement
from sources.scan_snake_vision import scan_snake_vision
from sources.utils.get_window_size import get_window_size
from sources.utils.is_game_win_or_lost import is_game_win_or_lost
from sources.utils.print_snake_vision import print_snake_vision
from sources.utils.should_quit_game import should_quit_game


def main():
    pygame.init()

    # Gets the window's dimensions and corresponding pixel length of one cell
    (win_w, win_h), cell_length_px = get_window_size(GL_BOARD_SIZE_IN_CELL)

    # Creates a Surface object from the window's dimensions
    surface: Surface = pygame.display.set_mode((win_w, win_h))

    # Sets the window's name
    pygame.display.set_caption(GL_WINDOW_NAME)

    # Initialises Board object
    board: Board = Board(win_w, win_h, cell_length_px)

    # Creates a Clock object that is used to refresh the screen a limited
    # amount of times per second
    clock: Clock = pygame.time.Clock()

    # Boolean that represents if the game must be quited or not
    quit_game: bool = False

    # Associates each keyboard movement key with its matching Direction
    MOVE_MAP = {
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT
    }

    while not quit_game and not is_game_win_or_lost(board):
        for event in pygame.event.get():
            if should_quit_game(event):
                quit_game = True

            # TODO décoreller mouvement des touches pour que l'IA puisse bouger
            if event.type == pygame.KEYDOWN and event.key in MOVE_MAP:
                handle_movement(board, MOVE_MAP[event.key])

        if is_game_win_or_lost(board):
            continue

        draw_game(surface, board)

        pygame.display.update()

        # TODO remove this tick for training
        clock.tick(60)

    pygame.quit()


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(e)
