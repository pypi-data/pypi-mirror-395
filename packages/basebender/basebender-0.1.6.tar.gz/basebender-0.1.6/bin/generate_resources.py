#!/usr/bin/env python3
"""
This script generates Python resource files from Qt .qrc files using pyside6-rcc.
It is intended to be run as part of the project's build process, e.g., by Poetry.
"""

import os
import subprocess
import sys


def main():
    """
    Main function to generate application resources.

    It defines paths, ensures the output directory exists, and then
    executes the pyside6-rcc command to compile the .qrc file into a Python module.
    Handles FileNotFoundError for missing pyside6-rcc and CalledProcessError
    for command execution failures, providing informative error messages.
    """
    # Define paths relative to the project root.
    # When 'poetry build' executes this script, it runs from the project root.
    qrc_file = "src/basebender/rebaser/resources/app_resources.qrc"
    output_dir = "src/basebender/rebaser/generated"
    output_file = os.path.join(output_dir, "app_resources_rc.py")

    print(f"Starting resource generation from: {qrc_file}")
    print(f"Output will be saved to: {output_file}")

    # 1. Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        # 2. Construct the command to run pyside6-rcc
        # We need 'poetry run' here because pyside6-rcc might not be directly in the PATH
        # when this script is executed in certain environments (e.g., GitHub Actions).
        command = ["poetry", "run", "pyside6-rcc", qrc_file, "-o", output_file]

        print(f"Executing command: {' '.join(command)}")

        # 3. Run the command using subprocess
        # 'check=True' will raise a CalledProcessError if the command returns a non-zero exit code.
        # 'capture_output=True' captures stdout and stderr.
        # 'text=True' decodes stdout/stderr as text.
        result = subprocess.run(
            command, check=True, capture_output=True, text=True
        )

        if result.stdout:
            print("pyside6-rcc stdout:")
            print(result.stdout)
        if result.stderr:
            print("pyside6-rcc stderr:")
            print(result.stderr)

        print(f"Successfully generated {output_file}")

    except FileNotFoundError:
        print(
            "'pyside6-rcc' command not found. "
            "Skipping the re-generation of the icons",
            file=sys.stdout,
        )
        print("You can install it with: poetry add pyside6", file=sys.stderr)
    except subprocess.CalledProcessError as process_error:
        print(
            "Skipping the re-generation of the icons",
            file=sys.stdout,
        )
        print(f"Command: {' '.join(process_error.cmd)}", file=sys.stderr)
        print(f"Stderr: {process_error.stderr}", file=sys.stderr)
    except Exception as general_error:  # pylint: disable=W0718
        # Catching a broad exception here as a final fallback for unexpected issues.
        print(f"An unexpected error occurred: {general_error}", file=sys.stderr)
        sys.exit(1)  # Exit with an error code


if __name__ == "__main__":
    main()
