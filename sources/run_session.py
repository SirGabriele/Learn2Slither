import pygame

from sources.agent.agent import Agent
from sources.classes.board import Board
from sources.classes.renderer import Renderer
from sources.enums.direction_enum import Direction
from sources.handle_movement import handle_movement
from sources.utils.get_snake_vision import get_snake_vision
from sources.utils.is_game_win_or_lost import is_game_win_or_lost
from sources.utils.print_snake_vision import print_snake_vision
from sources.utils.should_quit_game import should_quit_game


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
                       is_learning_mode=agent.learning_mode,
                       action=None)

    if renderer is not None:
        renderer.update(snake=board.snake, apples=board.apples)

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
        elif debug_mode:
            for pygame_event in pygame.event.get():
                if should_quit_game(pygame_event):
                    quit_game = True
                    continue

                if (pygame_event.type == pygame.KEYDOWN and pygame_event.key
                        in MOVE_MAP):
                    handle_movement(board, MOVE_MAP[pygame_event.key])
                    board.snake.digest_apple()

                    game_state = get_snake_vision(board)
                    print_snake_vision(cross_view=game_state,
                                       is_learning_mode=agent.learning_mode,
                                       action=MOVE_MAP[pygame_event.key])

            if quit_game:
                continue
        #     if visual_mode:
        #         pygame_event = pygame.event.wait()
        #
        #         if should_quit_game(pygame_event):
        #             quit_game = True
        #             continue
        #
        #         if is_step_validated(pygame_event):
        #             run_game = True

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

        if renderer is not None and board.snake.is_dead() is False:
            renderer.update(snake=board.snake,
                            apples=board.apples,
                            tick=True)

    # Decreases epsilon so that the agent explores less and less overtime
    # agent.lower_epsilon()

    return len(board.snake.segments.body_board_coords)
