from easy_logging.config import FormatterConfig


class TestConfig:
    """Test the FormatterConfig class."""

    def test_default_config(self) -> None:
        """Test the default configuration.

        This test ensures that the default configuration is as expected.
        """
        config = FormatterConfig()
        assert config.template == ("[{time}] {level_icon} {level} |"
                                   " {message} {context} ({filename}:{lineno})")
        assert config.date_format == "%H:%M:%S"
        assert config.use_colors is True
        assert config.json_output is False
        assert config.shorten_paths is True
        assert config.exclude_fields == ["color", "icon"]
        assert config.use_icons is False

    def test_json_output(self) -> None:
        """Test the json_output configuration.

        This test ensures that the json_output configuration is as expected.
        """
        config = FormatterConfig(json_output=True)
        assert config.json_output is True
        assert config.use_colors is False

    def test_shorten_paths(self) -> None:
        """Test the shorten_paths configuration.

        This test ensures that the shorten_paths configuration is as expected.
        """
        config = FormatterConfig(shorten_paths=True)
        assert config.shorten_paths is True
        config = FormatterConfig(shorten_paths=False)
        assert config.shorten_paths is False

    def test_exclude_fields(self) -> None:
        """Test the exclude_fields configuration.

        This test ensures that the exclude_fields configuration has the expected values.
        """
        config = FormatterConfig(exclude_fields=["color"])
        assert config.exclude_fields == ["color"]

    def test_use_icons(self) -> None:
        """Test the use_icons configuration.

        This test ensures that the use_icons configuration is as expected.
        """
        config = FormatterConfig(use_icons=True)
        assert config.use_icons is True

    def test_json_disables_colors_automatically(self) -> None:
        """Test that JSON output disables colors automatically.

        This test ensures that JSON output disables colors automatically.
        """
        config = FormatterConfig(json_output=True, use_colors=True)

        assert config.json_output is True
        assert config.use_colors is False
