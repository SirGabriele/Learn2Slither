import pygame

from numpy import ndarray
from pygame import Surface

from constants import GL_BOARD_SIZE_IN_CELL, GL_PROGRAM_NAME

from sources.agent.agent import Agent
from sources.classes.board import Board
from sources.draw_game import draw_game
from sources.enums.direction_enum import Direction
from sources.handle_movement import handle_movement
from sources.get_game_state import get_game_state
from sources.utils.get_window_size import get_window_size
from sources.utils.is_game_win_or_lost import is_game_win_or_lost
from sources.utils.print_snake_vision import print_snake_vision
from sources.utils.should_quit_game import should_quit_game


def run_session(agent: Agent, visual_mode: bool, step_by_step: bool):
    pygame.init()

    surface: Surface | None = None

    # Gets the window's dimensions and corresponding pixel length of one cell
    (win_w, win_h), cell_length_px = get_window_size(GL_BOARD_SIZE_IN_CELL)

    if visual_mode:
        # Sets the window's name
        pygame.display.set_caption(GL_PROGRAM_NAME)

        # Creates a Surface object from the window's dimensions
        surface = pygame.display.set_mode((win_w, win_h))

        # Creates a Clock object that is used to refresh the screen a limited
        # amount of times per second
        # clock = pygame.time.Clock()

    # Initialises Board object
    board: Board = Board(win_w, win_h, cell_length_px)

    # Boolean that represents if the game must be quited or not
    quit_game: bool = False
    # Boolean that represents if the game is waiting for an input

    # Associates each keyboard movement key with its matching Direction
    MOVE_MAP = {
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT
    }

    # Prints the initial snake vision
    game_state = get_game_state(board)
    print_snake_vision(game_state)

    if visual_mode and surface is not None:
        draw_game(surface, board)
        pygame.display.update()

    while not quit_game and not is_game_win_or_lost(board):
        pygame_event = pygame.event.wait()

        if should_quit_game(pygame_event):
            quit_game = True
            continue

        # TODO supprimer ce if
        if pygame_event.type == pygame.KEYDOWN and pygame_event.key in MOVE_MAP:
            handle_movement(board, MOVE_MAP[pygame_event.key])
            game_state: ndarray = get_game_state(board)
            print_snake_vision(game_state)
            chosen_movement = agent.get_next_movement(game_state)

        # run_game = not step_by_step
        #
        # if step_by_step:
        #     run_game = False
        #
        #     if is_step_validated(pygame_event):
        #         run_game = True
        #
        # if run_game:
        #     game_state: ndarray = get_game_state(board)
        #     chosen_movement = agent.get_next_movement(game_state)
        #     handle_movement(board, chosen_movement)
        #     print_snake_vision(game_state)

        if visual_mode and surface is not None:
            draw_game(surface, board)
            pygame.display.update()

    pygame.quit()
