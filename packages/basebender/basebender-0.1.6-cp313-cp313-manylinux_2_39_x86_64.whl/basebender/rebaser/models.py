"""
This module defines data models used across the BaseBender application.

It includes the `DigitSet` dataclass, which represents a set of characters
used in a positional number system, along with its name and source.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class DigitSet:
    """
    Represents a digit set used in a positional number system.

    Attributes:
        name (str): The human-readable name of the digit set (e.g., "Binary",
                    "Decimal").
        digits (str): The string containing all unique characters that form the
                      digit set, ordered by their value (e.g., "01" for binary,
                      "0123456789" for decimal).
        source (str): The origin of the digit set (e.g., "package", "system",
                      "user", "cli_input", "gui_input").
    """

    name: str
    digits: str
    source: str
