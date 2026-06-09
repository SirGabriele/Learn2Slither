import pygame
import traceback

from argparse import ArgumentParser
from pathlib import Path

from pygame import Surface

from constants import GL_BOARD_SIZE_IN_CELL, GL_PROGRAM_NAME
from sources.agent.agent import Agent
from sources.run_session import run_session
from sources.parser.init_parser import init_parser
from sources.utils.get_window_size import get_window_size


def main():
    parser: ArgumentParser = init_parser()
    args = parser.parse_args()

    if args.learning == "on" and args.save is None:
        parser.error(
            "Arguments conflict: '--save' is required when learning is "
            "'on'.")

    if args.learning == "off" and args.save is not None:
        parser.error(
            "Arguments conflict: Cannot use '--save' when learning is 'off'.")

    if args.visual == "on" and args.step_by_step:
        parser.error(
            "Arguments conflict: Cannot use 'step by step mode' when visual "
            "mode is 'on'.")

    sessions: int = args.session
    visual_mode: bool = args.visual == "on"
    save_file: Path | None = args.save
    load_file: Path | None = args.load
    learning_mode: bool = args.learning == "on"
    step_by_step: bool = args.step_by_step

    agent: Agent = Agent(save_file, load_file, learning_mode)

    pygame.init()

    surface: Surface | None = None
    # Gets the window's dimensions and corresponding pixel length of one cell
    (win_w, win_h), cell_length_px = get_window_size(GL_BOARD_SIZE_IN_CELL)

    if visual_mode:
        # Sets the window's name
        pygame.display.set_caption(GL_PROGRAM_NAME)

        # Creates a Surface object from the window's dimensions
        surface = pygame.display.set_mode((win_w, win_h))

    try:
        for session in range(sessions):
            print(f"Running session {session + 1}/{sessions}")
            run_session(agent=agent,
                        visual_mode=visual_mode,
                        step_by_step=step_by_step,
                        surface=surface,
                        win_w=win_w,
                        win_h=win_h,
                        cell_length_px=cell_length_px
                        )
        print()
    finally:
        pygame.quit()

    if save_file:
        agent.save(save_file)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        separator = "=" * 60

        print(separator)
        print("Full trace:")
        traceback.print_exc()
        print(separator)
