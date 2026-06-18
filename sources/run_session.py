import numpy as np
import pygame

from sources.agent.agent import Agent
from sources.agent.calculate_reward import calculate_reward
from sources.classes.board import Board
from sources.classes.renderer import Renderer
from sources.enums.direction_enum import Direction
from sources.utils.convert_game_state_to_bitmap import \
    convert_game_state_to_bitmap
from sources.utils.handle_movement import handle_movement
from sources.utils.get_snake_vision import get_snake_vision
from sources.utils.is_game_win_or_lost import is_game_win_or_lost
from sources.utils.is_step_validated import is_step_validated
from sources.utils.print_snake_vision import print_snake_vision
from sources.utils.process_step_limit import process_step_limit
from sources.utils.should_quit_game import should_quit_game


def _flush_event_queue() -> bool:
    quit_game = False

    for pygame_event in pygame.event.get():
        if should_quit_game(pygame_event):
            quit_game = True

    return quit_game


def _handle_debug_mode(board: Board,
                       move_map: dict[int, Direction]) -> bool:
    quit_game = False

    for pygame_event in pygame.event.get():
        if should_quit_game(pygame_event):
            quit_game = True
            continue

        if (pygame_event.type == pygame.KEYDOWN and pygame_event.key
                in move_map):
            handle_movement(board, move_map[pygame_event.key])
            board.snake.digest_apple()
            is_dead = board.snake.is_dead()

            if not is_dead:
                game_state = get_snake_vision(board)
                print_snake_vision(cross_view=game_state,
                                   action=move_map[pygame_event.key])

    return quit_game


def run_session(agent: Agent,
                renderer: Renderer | None,
                step_by_step: bool,
                debug_mode: bool) -> int:
    # Initialises Board.
    board: Board = Board()

    # Boolean that represents if the game must be quited or not.
    quit_game: bool = False

    # Prints the initial snake vision.
    game_state = get_snake_vision(board)
    print_snake_vision(cross_view=game_state,
                       action=None)

    if renderer is not None:
        renderer.update(snake=board.snake, apples=board.apples)

    step_limit: int = 0

    move_map: dict[int, Direction] = {
        pygame.K_w: Direction.UP,
        pygame.K_s: Direction.DOWN,
        pygame.K_a: Direction.LEFT,
        pygame.K_d: Direction.RIGHT
    }

    while not quit_game and not is_game_win_or_lost(board, step_limit,
                                                    debug_mode):
        # Lets the event queue flush to prevent the window from not responding.
        if renderer is not None and not debug_mode:
            quit_game = _flush_event_queue()

            if quit_game:
                continue

        run_game = not step_by_step and not debug_mode

        if step_by_step:
            if renderer is not None:
                pygame_event = pygame.event.wait()

                if should_quit_game(pygame_event):
                    quit_game = True
                    continue

                if is_step_validated(pygame_event):
                    run_game = True
        elif debug_mode:
            quit_game = _handle_debug_mode(board, move_map)

            if quit_game:
                continue

        if run_game:
            snake_vision: np.ndarray = get_snake_vision(board)
            game_state: str = (convert_game_state_to_bitmap(
                snake_vision, board.snake.segments.head).tostring())

            action: Direction = agent.get_next_movement(game_state)
            handle_movement(board, action)
            is_dead = board.snake.is_dead()

            if not is_dead:
                snake_vision: np.ndarray = get_snake_vision(board)
                new_game_state: str = (convert_game_state_to_bitmap(
                    snake_vision, board.snake.segments.head).tostring())
            else:
                new_game_state: str = ""

            reward = calculate_reward(is_dead, board.snake.eaten_apple)
            board.snake.digest_apple()

            step_limit = process_step_limit(step_limit, reward)

            agent.learn(game_state, new_game_state, reward, action, is_dead)

            if not is_dead:
                print_snake_vision(cross_view=snake_vision,
                                   action=action)

        if renderer is not None and not board.snake.is_dead():
            renderer.update(snake=board.snake,
                            apples=board.apples,
                            tick=True)

    # Decreases epsilon so that the agent explores less and less overtime.
    agent.lower_epsilon()

    return len(board.snake.segments.body_board_coords)
