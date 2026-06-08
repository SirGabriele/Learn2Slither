import traceback

from argparse import ArgumentParser
from pathlib import Path

from sources.agent.agent import Agent
from sources.run_session import run_session
from sources.parser.init_parser import init_parser


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

    sessions: int = args.session
    visual_mode: bool = args.visual == "on"
    save_file: Path | None = args.save
    load_file: Path | None = args.load
    learning_mode: bool = args.learning == "on"
    step_by_step: bool = args.step_by_step

    agent: Agent = Agent(save_file, load_file, learning_mode)

    for session in range(sessions):
        print(f"Running session {session + 1}/{sessions}")
        run_session(agent=agent, visual_mode=visual_mode,
                    step_by_step=step_by_step)
    print()

    if save_file:
        agent.save(save_file)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        pass
    except Exception as e:
        # TODO print traceback et trouver ce problème d'index
        # index -1 is out of bounds for axis 0 with size 0
        print("\n" + "=" * 50)
        print("CRITICAL ERROR DETECTED! Here is the full trace:")
        print("=" * 50)

        # This prints the exact file names, line numbers, and call stack
        traceback.print_exc()

        print("=" * 50 + "\n")
        # print(e)
