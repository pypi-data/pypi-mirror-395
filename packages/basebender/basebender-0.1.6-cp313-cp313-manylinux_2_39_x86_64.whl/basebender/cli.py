"""
This module provides a command-line interface (CLI) for the BaseBender tool.

It allows users to rebase strings between different digit sets, list available
digit sets, suggest digit sets for a given string, and launch a graphical user
interface or an API server.
"""

import argparse
import logging
import sys
from typing import Optional

import uvicorn

from basebender.gui.main_window import (  # Moved from conditional import
    run_gui,
)
from basebender.rebaser.digit_set_rebaser import DigitSetRebaser
from basebender.rebaser.digit_sets import (
    get_predefined_digit_sets,
    suggest_digit_sets,
)
from basebender.rebaser.models import DigitSet

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def list_digit_sets_cli() -> int:
    """
    Lists all available pre-defined digit sets to the console.

    Returns:
        An exit code (0 for success).
    """
    print("Pre-defined Digit Sets:")
    digit_sets = get_predefined_digit_sets()
    for digit_set_id, digit_set_info in digit_sets.items():
        print(
            f"  {digit_set_id} (Name: {digit_set_info.name}, "
            f"Source: {digit_set_info.source}): {digit_set_info.digits}"
        )
    return 0


def suggest_digit_sets_cli(input_string: str) -> int:
    """
    Suggests pre-defined digit sets based on characters in the input string.

    Args:
        input_string: The string for which to suggest digit sets.

    Returns:
        An exit code (0 for success).
    """
    suggestions = suggest_digit_sets(input_string)
    if suggestions:
        print(f"Suggested Digit Sets for '{input_string}':")
        for suggestion in suggestions:
            print(f"  - {suggestion}")
    else:
        print(f"No pre-defined digit sets suggested for '{input_string}'.")
    return 0


def perform_rebase_cli(
    input_string: Optional[str],
    output_digit_set_str: Optional[str],
    input_digit_set_str: Optional[str],
) -> int:
    """
    Performs the digit set rebase operation and prints the result to the console.

    This function handles the dynamic derivation of input and output digit sets
    from predefined sets or user-provided strings. It also includes error
    reporting for invalid operations.

    Args:
        input_string: The string to be rebased.
        output_digit_set_str: The identifier or string representation of the
            target digit set.
        input_digit_set_str: The identifier or string representation of the
            source digit set.

    Returns:
        An exit code (0 for success, 1 for error).
    """
    if not input_string:
        print("Rebased string: ")
        return 0

    digit_sets_data = get_predefined_digit_sets()
    input_digit_set_obj: Optional[DigitSet] = None
    output_digit_set_obj: Optional[DigitSet] = None

    # Determine input digit set
    if input_digit_set_str:
        if input_digit_set_str in digit_sets_data:
            input_digit_set_obj = digit_sets_data[input_digit_set_str]
        else:
            input_digit_set_obj = DigitSet(
                name="Provided", digits=input_digit_set_str, source="cli_input"
            )

    # Determine output digit set
    if output_digit_set_str:
        if output_digit_set_str in digit_sets_data:
            output_digit_set_obj = digit_sets_data[output_digit_set_str]
        else:
            output_digit_set_obj = DigitSet(
                name="Provided", digits=output_digit_set_str, source="cli_input"
            )

    try:
        rebaser = DigitSetRebaser(
            out_digit_set=output_digit_set_obj, in_digit_set=input_digit_set_obj
        )
        rebased_string = rebaser.rebase(input_string)
        print(f"Rebased string: {rebased_string}")
        return 0
    except ValueError as exc:
        logging.error("Error: Invalid digit set or rebase operation. %s", exc)
        return 1
    except IndexError as exc:
        logging.error(
            "Error: Digit set index out of bounds. This usually indicates an "
            "internal issue with digit set mapping. %s",
            exc,
        )
        return 1
    except Exception as exc:  # pylint: disable=broad-exception-caught
        # Catching broad exception as an isolation point for unexpected errors.
        logging.error("An unexpected error occurred during rebase: %s", exc)
        return 1


def main() -> None:
    """
    Main entry point for the BaseBender command-line interface.

    This function parses command-line arguments, handles various CLI operations
    like listing digit sets, suggesting digit sets, launching the GUI or API,
    and performing string rebase operations.
    """
    parser = argparse.ArgumentParser(
        description=(
            "BaseBender: A tool for rebaseing strings between different "
            "digit sets (positional number systems)."
        ),
        epilog="For more information, refer to the project's README.md.",
    )
    parser.add_argument(
        "input_string",
        nargs="?",
        default=None,
        help=(
            "The string to be rebased. Required unless --list-digit-sets, "
            "--suggest-digit-sets, --gui, or --api is used."
        ),
    )
    parser.add_argument(
        "output_digit_set",
        nargs="?",
        default=None,
        help=(
            "The target digit set string for the rebase operation. If "
            "omitted, the input string will be filtered based on the input "
            "digit set."
        ),
    )
    parser.add_argument(
        "input_digit_set",
        nargs="?",
        default=None,
        help=(
            "The source digit set string for the rebase operation. If "
            "omitted, the input digit set will be dynamically derived from "
            "the input string."
        ),
    )
    parser.add_argument(
        "-l",
        "--list-digit-sets",
        action="store_true",
        help=(
            "List all available pre-defined digit sets loaded from "
            "configuration files."
        ),
    )
    parser.add_argument(
        "-s",
        "--suggest-digit-sets",
        metavar="STRING",
        help=(
            "Suggest pre-defined digit sets that are relevant to the "
            "provided STRING based on its characters."
        ),
    )
    parser.add_argument(
        "--gui",
        action="store_true",
        help="Launch the graphical user interface for interactive rebaseing.",
    )
    parser.add_argument(
        "--api",
        action="store_true",
        help=(
            "Start the FastAPI server, providing a web API for rebase "
            "operations."
        ),
    )

    args = parser.parse_args()
    exit_code = 0

    if args.gui:
        run_gui()
    elif args.api:
        # Ensure the API module is importable from the current directory
        uvicorn.run(
            "basebender.api.main:APP", host="0.0.0.0", port=8000, reload=True
        )
    elif args.list_digit_sets:
        exit_code = list_digit_sets_cli()
    elif args.suggest_digit_sets:
        exit_code = suggest_digit_sets_cli(args.suggest_digit_sets)
    else:
        # If no specific action (list, suggest, gui, api) is requested, rebase
        if args.input_string is None and not (
            args.list_digit_sets
            or args.suggest_digit_sets
            or args.gui
            or args.api
        ):
            parser.error(
                (
                    "input_string is required for rebase when not using "
                    "--list-digit-sets, --suggest-digit-sets, --gui, or --api."
                )
            )
        exit_code = perform_rebase_cli(
            args.input_string, args.output_digit_set, args.input_digit_set
        )
    sys.exit(exit_code)


if __name__ == "__main__":
    main()
