import json
import logging
import os
import sys
import pytest
from pytest_mock import MockerFixture
from easy_logging.config import FormatterConfig
from easy_logging.formatter import EasyFormatter
from easy_logging.styling import Ansi


class TestEasyFormatter:
    """Test suite for the EasyFormatter class.

    Grouped by functionality.
    """

    @pytest.fixture
    def log_record(self) -> logging.LogRecord:
        """Create a generic LogRecord for testing."""
        record = logging.LogRecord(
            name="test_app",
            level=logging.INFO,
            pathname="/users/dev/project/src/main.py",
            lineno=42,
            msg="Test message",
            args=(),
            exc_info=None,
        )
        return record

    @pytest.fixture
    def log_record_with_context(
        self,
        log_record: logging.LogRecord,
    ) -> logging.LogRecord:
        """Create a generic LogRecord for testing."""
        record = log_record
        record.user_id = 99
        record.action = "login"
        return record

    def test_default_initialization(self, log_record: logging.LogRecord) -> None:
        """Verify the formatter works with zero config."""
        formatter = EasyFormatter()
        output = formatter.format(log_record)

        assert "Test message" in output
        assert "INFO" in output
        assert "{" not in output or "timestamp" not in output

    def test_json_formatting(self, log_record: logging.LogRecord) -> None:
        """Verify JSON mode outputs valid JSON with correct fields."""
        config = FormatterConfig(json_output=True)
        formatter = EasyFormatter(config=config)

        output = formatter.format(log_record)
        data = json.loads(output)

        assert data["level"] == "INFO"
        assert data["message"] == "Test message"
        assert data["line"] == 42
        assert "timestamp" in data
        assert "\033[" not in output

    def test_context_injection(
        self,
        log_record_with_context: logging.LogRecord,
    ) -> None:
        """Verify extra fields are injected correctly."""
        config = FormatterConfig(use_colors=True)
        self._test_context_injection(config, log_record_with_context)

    def test_context_injection_json(
        self,
        log_record_with_context: logging.LogRecord,
    ) -> None:
        """Verify extra fields are merged into top-level JSON."""
        config = FormatterConfig(json_output=True)
        self._test_context_injection(config, log_record_with_context)

    def _test_context_injection(
        self,
        config: FormatterConfig,
        log_record: logging.LogRecord,
    ) -> None:
        """Verify extra fields are injected correctly."""
        formatter = EasyFormatter(config=config)
        output = formatter.format(log_record)

        if config.json_output:
            data = json.loads(output)
            assert data["user_id"] == 99
            assert data["action"] == "login"
        else:
            assert "user_id" in output and "99" in output
            assert "action" in output and "login" in output

    def test_path_shortening(self, log_record: logging.LogRecord) -> None:
        """Verify absolute paths are converted to relative paths."""
        cwd = os.getcwd()
        log_record.pathname = os.path.join(cwd, "src/main.py")

        config = FormatterConfig(shorten_paths=True)
        formatter = EasyFormatter(config=config)

        output = formatter.format(log_record)

        assert "/users/dev/project/" not in output
        assert "main.py" in output

    def test_path_shortening_disabled(self, log_record: logging.LogRecord) -> None:
        """Verify absolute paths are not shortened."""
        cwd = os.getcwd()
        log_record.pathname = os.path.join(cwd, "src/main.py")

        config = FormatterConfig(shorten_paths=False)
        formatter = EasyFormatter(config=config)

        output = formatter.format(log_record)

        assert "src/main.py" in output
        assert cwd in output

    def test_path_shortening_failure_fallback(
        self, log_record: logging.LogRecord, mocker: MockerFixture,
    ) -> None:
        """Verify fallback to full path when relpath raises an Error."""
        config = FormatterConfig(shorten_paths=True)
        formatter = EasyFormatter(config=config)

        mocker.patch("os.path.relpath", side_effect=ValueError)
        output = formatter.format(log_record)

        assert "/users/dev/project/src/main.py" in output

    def test_icons_enabled(self, log_record: logging.LogRecord) -> None:
        """Verify icons are inserted into the output."""
        config = FormatterConfig(use_icons=True, template="{level_icon} {message}")
        formatter = EasyFormatter(config=config)

        output = formatter.format(log_record)

        assert "ℹ️" in output
        assert "Test message" in output

    def test_icons_unknown_level(self, log_record: logging.LogRecord) -> None:
        """Verify icons are inserted into the output."""
        config = FormatterConfig(use_icons=True, template="{level_icon} {message}")
        formatter = EasyFormatter(config=config)

        log_record.levelno = 99
        output = formatter.format(log_record)

        assert "•" in output
        assert "Test message" in output

    def test_ansi_coloring(self, log_record: logging.LogRecord) -> None:
        """Verify ANSI codes are injected for colored output."""
        config = FormatterConfig(use_colors=True)
        formatter = EasyFormatter(config=config)

        output = formatter.format(log_record)

        assert "\033[" in output

        assert Ansi.GREEN.value in output

    def test_exception_formatting(self, log_record: logging.LogRecord) -> None:
        """Verify exceptions are appended to the log."""
        try:
            _ = 1 / 0
        except ZeroDivisionError:
            # FIX: Use sys.exc_info() instead of os.sys.exc_info()
            log_record.exc_info = sys.exc_info()

        formatter = EasyFormatter()
        output = formatter.format(log_record)

        assert "ZeroDivisionError" in output
        assert "division by zero" in output

    def test_key_error_handling(self, log_record: logging.LogRecord) -> None:
        """Verify KeyError handling works as expected."""
        log_record.message = "This is a test message"
        config = FormatterConfig(template="{message} {non_existent_field}")
        formatter = EasyFormatter(config=config)
        output = formatter.format(log_record)

        assert "FORMAT ERROR" in output
        assert "message" in output

    def test_json_exception_formatting(self, log_record: logging.LogRecord) -> None:
        """Verify exceptions are included in JSON output."""
        try:
            _ = 1 / 0
        except ZeroDivisionError:
            log_record.exc_info = sys.exc_info()

        config = FormatterConfig(json_output=True)
        formatter = EasyFormatter(config=config)

        output = formatter.format(log_record)
        data = json.loads(output)

        assert "exception" in data
        assert "ZeroDivisionError" in data["exception"]
        assert "division by zero" in data["exception"]
