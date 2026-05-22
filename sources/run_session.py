import pygame

from numpy import ndarray
from pygame import Surface

from constants import GL_BOARD_SIZE_IN_CELL, GL_PROGRAM_NAME

from sources.agent.agent import Agent
from sources.agent.calculate_reward import calculate_reward
from sources.classes.board import Board
from sources.classes.apple import Apple
from sources.utils.convert_game_state_to_bitmap import \
    convert_game_state_to_bitmap
from sources.draw_game import draw_game
from sources.enums.direction_enum import Direction
from sources.handle_movement import handle_movement
from sources.get_snake_vision import get_snake_vision
from sources.utils.get_window_size import get_window_size
from sources.utils.is_game_win_or_lost import is_game_win_or_lost
from sources.utils.print_snake_vision import print_snake_vision
from sources.utils.should_quit_game import should_quit_game
from sources.utils.is_step_validated import is_step_validated


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
    # MOVE_MAP = {
    #     pygame.K_w: Direction.UP,
    #     pygame.K_s: Direction.DOWN,
    #     pygame.K_a: Direction.LEFT,
    #     pygame.K_d: Direction.RIGHT
    # }

    # Prints the initial snake vision
    game_state = get_snake_vision(board)
    print_snake_vision(game_state)

    if visual_mode and surface is not None:
        draw_game(surface, board)
        pygame.display.update()

    while not quit_game and not is_game_win_or_lost(board):
        run_game = not step_by_step

        # TODO supprimer ce if
        # if pygame_event.type == pygame.KEYDOWN and pygame_event.key in MOVE_MAP:
        #     handle_movement(board, MOVE_MAP[pygame_event.key])
        #     snake_vision: ndarray = get_snake_vision(board)
        #     print_snake_vision(game_state)

        if step_by_step:
            if visual_mode:
                pygame_event = pygame.event.wait()

                if should_quit_game(pygame_event):
                    quit_game = True
                    continue

                if is_step_validated(pygame_event):
                    run_game = True
            else:
                step_validation = input(
                    "Press Enter to advance step (or type 'q' to quit)...")
                if step_validation.strip().lower() == 'q':
                    quit_game = True
                    continue
                run_game = True
        else:
            for pygame_event in pygame.event.get():
                if should_quit_game(pygame_event):
                    quit_game = True
                    continue

            if quit_game:
                continue

        if run_game:
            snake_vision: ndarray = get_snake_vision(board)
            game_state: str = (convert_game_state_to_bitmap(snake_vision)
                               .tostring())

            action: Direction = agent.get_next_movement(game_state)
            # TODO enlever le return d'apple et créer une variable interne
            #  au snake
            eaten_apple: Apple | None = handle_movement(board, action)

            snake_vision: ndarray = get_snake_vision(board)
            new_game_state: str = (convert_game_state_to_bitmap(snake_vision)
                               .tostring())

            is_dead = board.snake.is_dead()
            reward = calculate_reward(is_dead, eaten_apple)

            agent.learn(game_state, new_game_state, reward, action)

            print_snake_vision(snake_vision)

        if visual_mode and surface is not None:
            draw_game(surface, board)
            pygame.display.update()

    # Decreases epsilon so that the agent explores less and less over time
    agent.lower_epsilon()
    pygame.quit()
