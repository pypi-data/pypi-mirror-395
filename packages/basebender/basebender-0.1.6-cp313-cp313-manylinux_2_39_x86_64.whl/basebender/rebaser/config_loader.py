"""
This module handles
loading and saving configuration for digit sets and UI state.

It defines paths for package, system, and user configuration files,
and provides functions to load digit sets from TOML files
and manage the application's UI state.
"""

import importlib.resources
import logging
import os
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

import toml

from .models import DigitSet

# Configure logging for this module
logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


def _get_config_paths() -> (
    Tuple[Path, Optional[Path], Optional[Path], Optional[Path]]
):
    """
    Determines the paths for package, system, and user configuration files.

    This function calculates the expected paths for `default_digit_sets.toml`
    (within the package), `digit_sets.toml` (system-wide and user-specific),
    and `ui_state.toml` (user-specific) based on the operating system.

    Returns:
        A tuple containing:
        - package_config_path (Path): Path to the default digit sets TOML file
          within the installed package.
        - system_config_path (Optional[Path]): Path to the system-wide digit
          sets TOML file, or None if not applicable for the OS.
        - user_config_path (Optional[Path]): Path to the user-specific digit
          sets TOML file, or None if not applicable for the OS.
        - ui_state_path (Optional[Path]): Path to the user-specific UI state
          TOML file, or None if not applicable for the OS.
    """
    package_config_path = (
        importlib.resources.files("basebender.rebaser.resources.data")
        / "default_digit_sets.toml"
    )

    # System config path (platform-dependent)
    if os.name == "posix":  # Linux, macOS
        system_config_path = Path("/etc") / "basebender" / "digit_sets.toml"
    elif os.name == "nt":  # Windows
        system_config_path = (
            Path(os.environ.get("PROGRAMDATA", "C:\\ProgramData"))
            / "basebender"
            / "digit_sets.toml"
        )
    else:
        system_config_path = None  # Fallback for unknown OS

    # User config path (platform-dependent)
    user_config_dir = None
    if os.name == "posix":
        user_config_dir = Path.home() / ".config" / "basebender"
    elif os.name == "nt":
        user_config_dir = (
            Path(os.environ.get("APPDATA", Path.home())) / "basebender"
        )

    user_config_path = (
        user_config_dir / "digit_sets.toml" if user_config_dir else None
    )
    ui_state_path = (
        user_config_dir / "ui_state.toml" if user_config_dir else None
    )

    return (
        package_config_path,
        system_config_path,
        user_config_path,
        ui_state_path,
    )


def load_digit_sets_from_toml(
    filepath: Path, source_type: str
) -> List[DigitSet]:
    """
    Loads digit sets from a TOML file, associating them with a given source type.

    Args:
        filepath: The path to the TOML file containing digit set definitions.
        source_type: A string indicating the source of these digit sets (e.g.,
                     "package", "system", "user").

    Returns:
        A list of `DigitSet` objects loaded from the file. Returns an empty list
        if the file is not found, is malformed, or contains invalid entries.
    """
    loaded_digit_sets: List[DigitSet] = []
    try:
        with open(filepath, "r", encoding="utf-8") as file_ptr:
            config = toml.load(file_ptr)

        digit_sets_data = config.get("digit_sets", [])
        if not isinstance(digit_sets_data, list):
            logging.warning(
                "'%s' in %s is not a list. Skipping.", "digit_sets", filepath
            )
            return loaded_digit_sets

        for digit_set_entry in digit_sets_data:
            if not isinstance(digit_set_entry, dict):
                logging.warning(
                    "Found non-dictionary item in 'digit_sets' in %s. Skipping: %s",
                    filepath,
                    digit_set_entry,
                )
                continue

            digit_set_name = digit_set_entry.get("name")
            digits = digit_set_entry.get("digits")

            if not isinstance(digit_set_name, str) or not digit_set_name:
                logging.warning(
                    "No 'name' found for a digit set entry in %s. Skipping: %s",
                    filepath,
                    digit_set_entry,
                )
                continue
            if not isinstance(digits, str) or not digits:
                logging.warning(
                    "Digit set entry '%s' in %s missing or invalid 'digits'. Skipping.",
                    digit_set_name,
                    filepath,
                )
                continue

            loaded_digit_sets.append(
                DigitSet(name=digit_set_name, digits=digits, source=source_type)
            )
    except FileNotFoundError:
        pass  # No digit sets from this file, which is fine
    except toml.TomlDecodeError as exc:
        logging.warning("Error decoding TOML file %s: %s", filepath, exc)
    except OSError as exc:  # Use OSError for modern Python
        logging.warning(
            "An unexpected error occurred while loading %s: %s", filepath, exc
        )
    return loaded_digit_sets


def get_all_digit_sets() -> Dict[str, DigitSet]:
    """
    Loads and merges digit sets from package, system, and user configurations.

    The loading order defines precedence: user configuration overrides system,
    and system overrides package defaults. Each digit set is assigned a unique
    ID based on its source and name (e.g., "package:ASCII").

    Returns:
        A dictionary where keys are unique IDs (e.g., "package:ASCII") and
        values are `DigitSet` objects.
    """
    package_path, system_path, user_path, _ = _get_config_paths()

    all_digit_sets_list: List[DigitSet] = []

    # Load package digit sets
    all_digit_sets_list.extend(
        load_digit_sets_from_toml(package_path, "package")
    )

    # Load system digit sets
    if system_path and system_path.exists():
        all_digit_sets_list.extend(
            load_digit_sets_from_toml(system_path, "system")
        )

    # Load user digit sets (highest precedence)
    if user_path and user_path.exists():
        all_digit_sets_list.extend(load_digit_sets_from_toml(user_path, "user"))

    # Convert list to a dictionary with unique IDs, handling precedence
    final_digit_sets: Dict[str, DigitSet] = {}
    for current_digit_set_obj in all_digit_sets_list:
        unique_id = (
            f"{current_digit_set_obj.source}:{current_digit_set_obj.name}"
        )
        final_digit_sets[unique_id] = current_digit_set_obj

    return final_digit_sets


def get_ui_state_path() -> Optional[Path]:
    """
    Returns the path to the user's UI state configuration file.

    This file is typically located in a user-specific configuration directory.

    Returns:
        A `Path` object pointing to the UI state file, or `None` if the
        user configuration directory cannot be determined for the current OS.
    """
    _, _, _, ui_state_path = _get_config_paths()
    return ui_state_path


def load_ui_state() -> Dict[str, Any]:
    """
    Loads the UI state from the user's configuration file.

    Returns:
        A dictionary containing the loaded UI state. Returns an empty dictionary
        if the file does not exist, is malformed, or an error occurs during loading.
    """
    ui_state_path = get_ui_state_path()
    if ui_state_path and ui_state_path.exists():
        try:
            with open(ui_state_path, "r", encoding="utf-8") as file_ptr:
                return toml.load(file_ptr)
        except toml.TomlDecodeError as exc:
            logging.warning(
                "Error decoding UI state TOML file %s: %s", ui_state_path, exc
            )
        except OSError as exc:  # Use OSError for modern Python
            logging.warning(
                "An unexpected error occurred while loading UI state from %s: %s",
                ui_state_path,
                exc,
            )
    return {}  # Return empty dict if file not found or error


def save_ui_state(state_data: Dict[str, Any]) -> None:
    """
    Saves the provided UI state data to the user's configuration file.

    The function ensures that the parent directory for the UI state file exists.
    Any errors during saving are logged.

    Args:
        state_data: A dictionary containing the UI state to be saved.
    """
    ui_state_path = get_ui_state_path()
    if ui_state_path:
        try:
            ui_state_path.parent.mkdir(parents=True, exist_ok=True)
            with open(ui_state_path, "w", encoding="utf-8") as file_ptr:
                toml.dump(state_data, file_ptr)
        except OSError as exc:  # Use OSError for modern Python
            logging.error(
                "Could not save UI state to %s: %s", ui_state_path, exc
            )


if __name__ == "__main__":
    # Example usage for testing
    print("--- Testing Digit Set Loading ---")
    digit_sets = get_all_digit_sets()
    print("Loaded Digit Sets:")
    for name_key, digit_set_obj in digit_sets.items():
        print(
            f"  {name_key}: {digit_set_obj.digits} "
            f"(Name: {digit_set_obj.name}, Source: {digit_set_obj.source})"
        )

    print("\n--- Testing UI State Saving/Loading ---")
    test_state = {
        "last_input": "Hello World",
        "last_source_digit_set": "package:ASCII",
        "last_target_digit_set": "package:Binary",
        "realtime_enabled": True,
    }
    print(f"Saving test UI state: {test_state}")
    save_ui_state(test_state)

    loaded_state = load_ui_state()
    print(f"Loaded UI state: {loaded_state}")
    assert (
        loaded_state == test_state
    ), "Loaded state does not match saved state!"

    # Clean up test state file
    ui_path = get_ui_state_path()  # pylint: disable=invalid-name
    if ui_path and ui_path.exists():
        os.remove(ui_path)
        print(f"Cleaned up {ui_path}")
    else:
        print("UI state file not found for cleanup.")
