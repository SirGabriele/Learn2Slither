from argparse import ArgumentParser
from pathlib import Path

from sources.agent.agent import Agent
from sources.run_session import run_session
from sources.parser.init_parser import init_parser


def main():
    parser: ArgumentParser = init_parser()
    args = parser.parse_args()
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
        print(e)
