"""Configuration class for the EasyFormatter."""
from dataclasses import dataclass, field

DEFAULT_FORMAT = ("[{time}] {level_icon} {level} |"
    " {message} {context} ({filename}:{lineno})")
DEFAULT_DATE_FORMAT = "%H:%M:%S"


@dataclass
class FormatterConfig:
    """Configuration object for the EasyFormatter.

    Attributes:
        template: The format string to use for the log message.
        date_format: The format string to use for the timestamp.
        use_colors: Whether to use colors in the output.
        json_output: Whether to output the log message as JSON.
        shorten_paths: Whether to shorten the paths in the log message.
        exclude_fields: A list of fields to exclude from the log message.
        use_icons: Whether to use icons in the output (e.g. ⚠️ for warnings).

    """

    template: str = DEFAULT_FORMAT
    date_format: str = DEFAULT_DATE_FORMAT
    use_colors: bool = True
    json_output: bool = False
    shorten_paths: bool = True

    exclude_fields: list[str] = field(default_factory=lambda: ["color", "icon"])
    use_icons: bool = False

    def __post_init__(self) -> None:
        """Post-initialization checks."""
        if self.json_output and self.use_colors:
            self.use_colors = False
