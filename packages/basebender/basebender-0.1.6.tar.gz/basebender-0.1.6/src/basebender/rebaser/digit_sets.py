"""
This module manages predefined digit sets and provides utility functions for
suggesting digit sets based on input strings.

It includes caching mechanisms for efficient retrieval of digit set data.
"""

from typing import Dict, List, Optional

from .config_loader import get_all_digit_sets
from .models import DigitSet

_PREDEFINED_DIGIT_SETS_CACHE: Optional[Dict[str, DigitSet]] = None


def get_predefined_digit_sets() -> Dict[str, DigitSet]:
    """
    Returns a dictionary of all loaded predefined digit sets.

    This function loads digit sets from various configuration sources (package,
    system, user) and caches the result for efficient retrieval on subsequent calls.
    The loading order defines precedence: user configuration overrides system,
    and system overrides package defaults.

    Returns:
        A dictionary where keys are unique IDs (e.g., "package:ASCII") and
        values are `DigitSet` objects.
    """
    global _PREDEFINED_DIGIT_SETS_CACHE  # pylint: disable=global-statement
    if _PREDEFINED_DIGIT_SETS_CACHE is None:
        _PREDEFINED_DIGIT_SETS_CACHE = get_all_digit_sets()
    return _PREDEFINED_DIGIT_SETS_CACHE


def suggest_digit_sets(input_string: str) -> List[str]:
    """
    Suggests predefined digit sets that the `input_string` might belong to.

    This function iterates through all known predefined digit sets and identifies
    those that contain all characters present in the `input_string`.

    Args:
        input_string: The string for which to suggest digit sets.

    Returns:
        A list of digit set IDs (strings) that are relevant to the input string.
        The list is currently not sophisticatedly ranked beyond basic matching.
    """
    predefined_digit_sets = get_predefined_digit_sets()
    suggestions: List[str] = []

    for digit_set_id, digit_set_info in predefined_digit_sets.items():
        if all(char in digit_set_info.digits for char in input_string):
            suggestions.append(digit_set_id)

    # Basic ordering: exact matches first (if any), then others.
    # For now, just return the list as is,
    # more sophisticated ranking can be added later.
    return suggestions


def main() -> None:
    """
    Main function for example usage and testing of digit set functionalities.
    """
    print("All Predefined Digit Sets:")
    for example_ds_id, example_ds_info in get_predefined_digit_sets().items():
        print(
            (
                f"  {example_ds_id} (Name: {example_ds_info.name}, "
                f"Source: {example_ds_info.source}): {example_ds_info.digits}"
            )
        )

    test_string_binary = "010110"  # pylint: disable=invalid-name
    test_string_decimal = "12345"  # pylint: disable=invalid-name
    test_string_hex = "DEADBEEF"  # pylint: disable=invalid-name
    test_string_mixed = "Hello World 123"  # pylint: disable=invalid-name

    print(
        (
            f"\nSuggestions for '{test_string_binary}': "
            f"{suggest_digit_sets(test_string_binary)}"
        )
    )
    print(
        (
            f"Suggestions for '{test_string_decimal}': "
            f"{suggest_digit_sets(test_string_decimal)}"
        )
    )
    print(
        (
            f"Suggestions for '{test_string_hex}': "
            f"{suggest_digit_sets(test_string_hex)}"
        )
    )
    print(
        (
            f"Suggestions for '{test_string_mixed}': "
            f"{suggest_digit_sets(test_string_mixed)}"
        )
    )


if __name__ == "__main__":
    main()
