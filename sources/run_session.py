import pygame

from numpy import ndarray
from pygame import Surface
from pygame.time import Clock

from constants import GL_BOARD_SIZE_IN_CELL, GL_FRAME_PER_SECOND, \
    GL_PROGRAM_NAME

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
from sources.utils.is_step_validated import is_step_validated
from sources.utils.print_snake_vision import print_snake_vision
from sources.utils.process_step_limit import process_step_limit
from sources.utils.should_quit_game import should_quit_game


def run_session(agent: Agent,
                visual_mode: bool,
                step_by_step: bool,
                surface: Surface | None,
                win_w: int,
                win_h: int,
                cell_length_px: int):
    clock: Clock | None = None

    if visual_mode:
        # Creates a Clock object that is used to refresh the screen a limited
        # amount of times per second
        clock = Clock()

    # Initialises Board object
    board: Board = Board(win_w, win_h, cell_length_px)

    # Boolean that represents if the game must be quited or not
    quit_game: bool = False

    # Prints the initial snake vision
    # game_state = get_snake_vision(board)
    # print_snake_vision(game_state)

    if visual_mode and surface is not None:
    #     draw_game(surface, board)
        pygame.display.update()

    step_limit: int = 0

    MOVE_MAP = {
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT
    }

    while not quit_game and not is_game_win_or_lost(board, step_limit):
        # run_game = not step_by_step

        if step_by_step:
            pass
        #     if visual_mode:
        #         pygame_event = pygame.event.wait()
        #
        #         if should_quit_game(pygame_event):
        #             quit_game = True
        #             continue
        #
        #         if is_step_validated(pygame_event):
        #             run_game = True
        else:
            for pygame_event in pygame.event.get():
                if (pygame_event.type == pygame.KEYDOWN and pygame_event.key
                        in MOVE_MAP):
                    handle_movement(board, MOVE_MAP[pygame_event.key])
                if should_quit_game(pygame_event):
                    quit_game = True
                    continue

            if quit_game:
                continue

        # if run_game:
            # snake_vision: ndarray = get_snake_vision(board)
            # game_state: str = (convert_game_state_to_bitmap(snake_vision)
            #                    .tostring())
            #
            # action: Direction = agent.get_next_movement(game_state)
            # eaten_apple: Apple | None = handle_movement(board, action)
            #
            # snake_vision: ndarray = get_snake_vision(board)
            # new_game_state: str = (convert_game_state_to_bitmap(snake_vision)
            #                        .tostring())
            #
            # is_dead = board.snake.is_dead()
            # reward = calculate_reward(is_dead, eaten_apple)
            #
            # step_limit = process_step_limit(step_limit, reward)
            #
            # agent.learn(game_state, new_game_state, reward, action)
            #
            # print_snake_vision(snake_vision, action)

        # if visual_mode and surface is not None and clock is not None:
        #     # if visual_mode and surface is not None:
        #     draw_game(surface, board)
            pygame.display.update()
            clock.tick(GL_FRAME_PER_SECOND)

    # Decreases epsilon so that the agent explores less and less overtime
    # agent.lower_epsilon()
