"""Styling utilities for the EasyFormatter."""
import logging
from dataclasses import dataclass, field
from enum import Enum


class Ansi(str, Enum):
    """Standard ANSI escape codes for terminal styling.

    Inherits from str so they can be concatenated directly.

    Example:
        >>> Ansi.RED + "Hello, world!" + Ansi.RESET
        '\\033[31mHello, world!\\033[0m'

    """

    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"

    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    WHITE = "\033[37m"


@dataclass
class Theme:
    """Configuration object for the EasyFormatter.

    Attributes:
        default_color: The default color for log messages.
        level_colors: A dictionary mapping log levels to colors.

    ## Methods
        get_color: Get the color for a given log level.
        style_text: Style a text string with the appropriate color and weight.

    Example:
        >>> theme = Theme(
        ...     level_colors={
        ...         logging.DEBUG: Ansi.CYAN,
        ...         logging.INFO: Ansi.GREEN,
        ...         logging.WARNING: Ansi.YELLOW,
        ...         logging.ERROR: Ansi.RED,
        ...         logging.CRITICAL: Ansi.MAGENTA,
        ...     },
        ... )
        >>> theme.get_color(logging.DEBUG)
        '\\033[36m'
        >>> theme.style_text("Hello, world!", logging.INFO)
        '\\033[32mHello, world!\\033[0m'

    """

    default_color: Ansi = Ansi.WHITE

    level_colors: dict[int, Ansi] = field(default_factory=dict)

    def get_color(self, level: int) -> str:
        """Get the color for a given log level.

        Args:
            level (int): The log level as an integer.

        Returns:
            str: The color for the log level.

        """
        return self.level_colors.get(level, self.default_color).value

    def style_text(self, text: str, level: int, bold: bool = False) -> str:
        """Style a text string with the appropriate color and weight.

        Args:
            text (str): The text to style.
            level (int): The log level as an integer.
            bold (bool, optional): Whether to use bold weight. Defaults to False.

        Returns:
            str: The styled text.

        """
        color = self.get_color(level)
        weight = Ansi.BOLD.value if bold else ""
        return f"{weight}{color}{text}{Ansi.RESET.value}"


DEFAULT_THEME = Theme(
    level_colors={
        logging.DEBUG: Ansi.CYAN,
        logging.INFO: Ansi.GREEN,
        logging.WARNING: Ansi.YELLOW,
        logging.ERROR: Ansi.RED,
        logging.CRITICAL: Ansi.MAGENTA,
    },
)
