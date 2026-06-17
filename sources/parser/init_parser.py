import argparse
import json
import os
import re

from argparse import ArgumentParser, ArgumentTypeError
from json import JSONDecodeError
from pathlib import Path

from constants import GL_PROGRAM_NAME


def _assert_json_content_format_valid(path: Path) -> None:
    try:
        with open(path, "r") as file:
            data = json.load(file)
    except JSONDecodeError as e:
        raise ArgumentTypeError(f"'{path}' is not a valid json file") from e

    if not isinstance(data, dict):
        raise ArgumentTypeError(
            f"Format Error: Root structure must be a JSON object (dict). "
            f"Got {type(data)}."
        )

    # BitMap allocates memory byte by byte. Since BitIndex has 12 elements,
    # the map will be padded with 4 '0' at the front.
    BINARY_KEY_EXPR = re.compile(r"^0{4}[01]{12}$")

    for key, value in data.items():
        if not BINARY_KEY_EXPR.match(key):
            raise ArgumentTypeError(
                f"Format Error: Key '{key}' is invalid. "
                f"Must be a 16-digit number containing only 0s "
                "and 1s."
            )
        elif not isinstance(value, list):
            raise ArgumentTypeError(
                f"Format Error: Value must be a list. "
                f"For key {key}, got {type(value).__name__}"
            )
        elif len(value) != 4:
            raise ArgumentTypeError(
                "Format Error: Value must contains 4 values. "
                f"For key {key}, got {len(value)}."
            )
        elif not all(isinstance(v, (int, float)) for v in value):
            raise ArgumentTypeError(
                "Format Error: Value must be numeric. "
                f"For key {key}, got {value}"
            )


def _save_file_valid(path_str: str) -> Path:
    path = Path(path_str)

    try:
        # Creates parent directories if needed.
        path.parent.mkdir(parents=True, exist_ok=True)

        # Creates file if it does not exist.
        path.touch(exist_ok=True)
    except OSError as e:
        raise ArgumentTypeError(
            f"Can not create file or directories for '{path}': {e}"
        )

    if not path.is_file():
        raise ArgumentTypeError(f"'{path}' is not a file")
    elif not os.access(path, os.W_OK):
        raise ArgumentTypeError(f"File '{path}' does not grant write rights")

    return path


def _load_file_valid(path_str: str) -> Path:
    path = Path(path_str)

    if not path.exists():
        raise ArgumentTypeError(f"'{path}' does not exist")
    elif not path.is_file():
        raise ArgumentTypeError(f"'{path}' is not a file")
    elif not os.access(path, os.R_OK):
        raise ArgumentTypeError(f"File '{path}' does not grant read rights")

    _assert_json_content_format_valid(path)

    return path


def _add_arg_load(parser: ArgumentParser) -> None:
    load_help_desc: str = ("file from which the model will be initialised ("
                           "Path)")

    parser.add_argument("--load", type=_load_file_valid,
                        default=None, metavar="/path/to/load/file",
                        help=load_help_desc)


def _add_arg_save(parser: ArgumentParser) -> None:
    save_help_desc: str = ("file in which the resulting model will be "
                           "saved (Path). Requires '-l on' / '--learning on'")

    parser.add_argument("--save", type=_save_file_valid,
                        default=None, metavar="/path/to/save/file",
                        help=save_help_desc)


def _add_arg_debug(parser: ArgumentParser) -> None:
    help_desc: str = ("debug mode allows the user the play the game. Requires "
                      "'-v on' / '--visual on'")

    parser.add_argument("-d", "--debug",
                        action="store_true", default=False, help=help_desc)


def _add_arg_step_by_step(parser: ArgumentParser) -> None:
    help_desc: str = ("if visual mode is on, will wait for a user input "
                      "between each step. Requires '-v off' / '--visual off'")

    parser.add_argument("-sbs", "--step-by-step",
                        action="store_true", default=False, help=help_desc)


def _add_arg_learning(parser: ArgumentParser) -> None:
    help_desc: str = ("if the model should learn from each session. Requires "
                      "'--save' to be specified")

    parser.add_argument("-l", "--learning", choices=["on", "off"],
                        default="off", help=help_desc)


def _add_arg_visual(parser: ArgumentParser) -> None:
    help_desc: str = ("visual mode on means a window will render the game "
                      "state. Not compatible with '-sbs' / '--step-by-step'")

    parser.add_argument("-v", "--visual", choices=["on", "off"],
                        required=True, help=help_desc)


def _add_arg_session(parser: ArgumentParser) -> None:
    help_desc: str = "number of sessions to run (integer)"

    parser.add_argument("-s", "--session", type=int,
                        metavar="N", required=True,
                        help=help_desc)


def init_parser() -> ArgumentParser:
    parser = argparse.ArgumentParser(prog=GL_PROGRAM_NAME)

    _add_arg_session(parser)
    _add_arg_visual(parser)
    _add_arg_save(parser)
    _add_arg_load(parser)
    _add_arg_learning(parser)
    _add_arg_step_by_step(parser)
    _add_arg_debug(parser)

    return parser
