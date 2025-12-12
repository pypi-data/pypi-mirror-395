"""The EasyFormatter class for formatting log messages."""

import logging
from .config import FormatterConfig
from datetime import datetime
from .styling import Ansi, Theme, DEFAULT_THEME
import os
import json
from typing import Any


class EasyFormatter(logging.Formatter):
    """The EasyFormatter class for formatting log messages.

    This class extends the standard logging.Formatter class to provide
    additional functionality for formatting log messages.

    Attributes:
        config: The configuration object for the formatter.

    Methods:
        format: Format a log message.

    """

    ICONS = {
        logging.CRITICAL: "💥",
        logging.ERROR: "❌",
        logging.WARNING: "⚠️ ",
        logging.INFO: "ℹ️ ",
        logging.DEBUG: "🐛",
    }

    def __init__(
        self,
        config: FormatterConfig | None = None,
        theme: Theme | None = None,
    ) -> None:
        """Initialize the EasyFormatter.

        Args:
            config (FormatterConfig): The configuration object for the formatter.
            theme (Theme, optional): The theme to use for styling. Defaults to None.

        """
        super().__init__()
        self.config = config or FormatterConfig()
        self.theme = theme or DEFAULT_THEME

        template = self.config.template

        if self.config.use_colors:
            template = self._style_static_template(template)

        self._fmt_template = template

    def format(self, record: logging.LogRecord) -> str:
        """Format a log message.

        Args:
            record (logging.LogRecord): The log record to format.

        Returns:
            str: The formatted log message.

        """
        record.asctime = self.formatTime(record, self.config.date_format)

        context = self._get_context_fields(record)

        if self.config.json_output:
            return self._format_json(record, context)

        return self._format_text(record, context)

    def _format_text(self, record: logging.LogRecord, context: dict[str, Any]) -> str:
        """Format the text part of a log message.

        Apply dynamic coloring to log level if enabled.

        Args:
            record (logging.LogRecord): The log record to format.
            context (dict[str, Any]): The context fields for the log record.

        Returns:
            str: The formatted text.

        """
        level_text = record.levelname
        if self.config.use_colors:
            level_text = self.theme.style_text(level_text, record.levelno)

        icon = ""
        if self.config.use_icons:
            icon = self._get_level_icon(record.levelno)

        context_str = ""
        if context:
            parts = []
            for k, v in context.items():
                val_str = str(v)
                if self.config.use_colors:
                    k = f"{Ansi.DIM.value}{k}{Ansi.RESET.value}"
                parts.append(f"{k}={val_str}")
            context_str = " ".join(parts)

        try:
            log_str = self._fmt_template.format(
                level=level_text,
                level_icon=icon,
                context=context_str,
                message=record.getMessage(),
                time=record.asctime,
                name=record.name,
                lineno=record.lineno,
                filename=self._format_path(record.pathname),
            )
        except KeyError as e:
            log_str = f"[FORMAT ERROR] Missing key: {e} | {record.getMessage()}"

        if record.exc_info:
            exc_text = self.formatException(record.exc_info)
            log_str += f"\n{exc_text}"

        return log_str

    def _format_json(self, record: logging.LogRecord, context: dict[str, Any]) -> str:
        """Serialize the log record to a JSON string.

        Args:
            record (logging.LogRecord): The log record to serialize.
            context (dict[str, Any]): The context fields for the log record.

        Returns:
            str: The JSON string.

        """
        log_obj = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "message": record.getMessage(),
            "logger": record.name,
            "file": self._format_path(record.pathname),
            "line": record.lineno,
            **context,
        }

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        return json.dumps(log_obj, default=str)

    def _style_static_template(self, template: str) -> str:
        """Wrap known static fields in color codes automatically.

        Args:
            template (str): The template to style.

        Returns:
            str: The styled template.

        """
        from .styling import Ansi

        style_map = {
            "{time}": f"{Ansi.DIM.value}{{time}}{Ansi.RESET.value}",
            "{name}": f"{Ansi.MAGENTA.value}{{name}}{Ansi.RESET.value}",
            "{filename}": f"{Ansi.CYAN.value}{{filename}}{Ansi.RESET.value}",
            "{lineno}": f"{Ansi.CYAN.value}{{lineno}}{Ansi.RESET.value}",
        }

        for field, styled_field in style_map.items():
            if field in template:
                template = template.replace(field, styled_field)

        return template

    def _get_context_fields(self, record: logging.LogRecord) -> dict[str, Any]:
        """Get the context fields for a log record.

        Args:
            record (logging.LogRecord): The log record to get context for.

        Returns:
            dict[str, Any]: The context fields for the log record.

        """
        standard_attrs = {
            "args",
            "asctime",
            "created",
            "exc_info",
            "exc_text",
            "filename",
            "funcName",
            "levelname",
            "levelno",
            "lineno",
            "module",
            "msecs",
            "message",
            "msg",
            "name",
            "pathname",
            "process",
            "processName",
            "relativeCreated",
            "stack_info",
            "thread",
            "threadName",
            "taskName",
        }

        context = {}
        for key, value in record.__dict__.items():
            if key not in standard_attrs and key not in self.config.exclude_fields:
                context[key] = value

        return context

    def _format_path(self, path: str) -> str:
        """Format a path by shortening it and removing the user's home directory.

        Args:
            path (str): The path to format.

        Returns:
            str: The formatted path, or the original path if shortening is disabled.

        """
        if not self.config.shorten_paths:
            return path

        try:
            path = os.path.abspath(os.path.expanduser(path))
            return os.path.relpath(path)
        except ValueError:
            return path

    def _get_level_icon(self, level: int) -> str:
        """Get the icon for a log level.

        Args:
            level (int): The log level.

        Returns:
            str: The icon for the log level.

        """
        if level in self.ICONS:
            return self.ICONS[level]
        return "•"
