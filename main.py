from statistics import mean

import pygame
import traceback

from argparse import ArgumentParser, Namespace
from pathlib import Path

from sources.classes.renderer import Renderer
from constants import GL_BOARD_SIZE_IN_CELL, GL_PROGRAM_NAME
from sources.agent.agent import Agent
from sources.run_session import run_session
from sources.parser.init_parser import init_parser
from sources.utils.get_window_dimensions import get_window_dimensions


def _handle_parser_errors(parser: ArgumentParser, args: Namespace) -> None:
    if args.learning == "on" and args.save is None:
        parser.error(
            "Arguments conflict: '--save' is required when learning is "
            "'on'.")

    if args.save is not None and args.learning == "off":
        parser.error(
            "Arguments conflict: Can not use '--save' when learning is 'off'.")

    if args.visual == "off" and args.step_by_step:
        parser.error(
            "Arguments conflict: Can not use 'step by step mode' when visual "
            "mode is 'off'.")

    if args.debug and args.visual == "off":
        parser.error(
            "Arguments conflict: Can not use 'debug mode' when visual "
            "mode is 'off'.")


def main():
    parser: ArgumentParser = init_parser()
    args: Namespace = parser.parse_args()

    _handle_parser_errors(parser, args)

    sessions: int = args.session
    visual_mode: bool = args.visual == "on"
    save_file: Path | None = args.save
    load_file: Path | None = args.load
    learning_mode: bool = args.learning == "on"
    step_by_step: bool = args.step_by_step
    debug_mode: bool = args.debug

    agent: Agent = Agent(save_file, load_file, learning_mode)

    # Initialises pygame.
    pygame.init()

    renderer: Renderer | None = None

    # Gets the window's dimensions and corresponding pixel length of one cell.
    win_w, win_h, cell_length_px = get_window_dimensions(GL_BOARD_SIZE_IN_CELL)

    if visual_mode:
        # Sets the window's name.
        pygame.display.set_caption(GL_PROGRAM_NAME)

        renderer = Renderer(visual_mode, (win_w, win_h, cell_length_px))

    snake_lengths: list[int] = []

    try:
        for session in range(sessions):
            print(f"Running session {session + 1}/{sessions}")
            snake_length = run_session(agent=agent,
                                       renderer=renderer,
                                       step_by_step=step_by_step,
                                       debug_mode=debug_mode)
            snake_lengths.append(snake_length)
            print(f"Session {session + 1} ended. Snake length: {snake_length}")
    finally:
        pygame.quit()

        if len(snake_lengths) != 0:
            print(f"Max snake length: {max(snake_lengths)}")
            print(f"Average snake length: {mean(snake_lengths):.2f}")

        if save_file:
            agent.save(save_file)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception:
        separator = "=" * 60

        print(separator)
        print("Full trace:")
        traceback.print_exc()
        print(separator)
