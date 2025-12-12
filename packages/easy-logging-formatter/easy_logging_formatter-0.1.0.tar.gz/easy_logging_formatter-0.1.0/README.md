# Easy Logger

**A highly customizable, zero-dependency logging formatter for Python.**

`easy-logger` bridges the gap between the standard library's complexity and the ease of use of third-party tools like Loguru. It creates beautiful, colored logs for development and structured JSON logs for production, all while using the standard `logging` module you already know.

## Features

* **Zero Dependencies:** No heavy libraries like `rich` or `pydantic`. Just pure Python.
* **Zero Config Defaults:** readable, colored logs out of the box.
* **Context Injection:** Automatically adds `extra={...}` fields to your logs without manual formatting.
* **Production Ready:** Switch to JSON output with a single boolean flag.
* **Smart Paths:** Automatically shortens absolute file paths (e.g., `src/main.py` instead of `/Users/me/projects/src/main.py`).

## Installation

### Pip/PyPI
```bash
pip install easy-logger
```

### uv
```bash
uv add easy-logger
```

## Usage

### Basic Usage

```python
import logging
from easy_logging import EasyFormatter

# Set up the handler
handler = logging.StreamHandler()
handler.setFormatter(EasyFormatter())

# Configure the logger
logger = logging.getLogger("app")
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("Hello, world!")
```

### Advanced Usage

```python
import logging
from easy_logging import EasyFormatter, FormatterConfig

config = FormatterConfig(
    template="[{time}] {level_icon} {level} | {message}",
    date_format="%H:%M:%S",
    use_colors=True,
    json_output=False,
    shorten_paths=True,
    exclude_fields=["color", "icon"],
    use_icons=False,
)
formatter = EasyFormatter(config=config)

handler = logging.StreamHandler()
handler.setFormatter(formatter)
logging.getLogger().addHandler(handler)
logging.getLogger().setLevel(logging.INFO)

logging.info("Hello, world!")
```

## Configuration

`easy-logger` provides a `FormatterConfig` class that allows you to customize the output of your logs. Here's an example of how to use it:

```python
from easy_logging import FormatterConfig

config = FormatterConfig(
    template="[{time}] {level_icon} {level} | {message}",
    date_format="%H:%M:%S",
    use_colors=True,
    json_output=False,
    shorten_paths=True,
    exclude_fields=["color", "icon"],
    use_icons=False,
)
```

The `FormatterConfig` class has the following attributes:

| Attribute | Type | Description |
| --- | --- | --- |
| `template` | str | The format string to use for the log message. |
| `date_format` | str | The format string to use for the timestamp. |
| `use_colors` | bool | Whether to use colors in the output. |
| `json_output` | bool | Whether to output the log message as JSON. |
| `shorten_paths` | bool | Whether to shorten the paths in the log message. |
| `exclude_fields` | list[str] | A list of fields to exclude from the log message. |
| `use_icons` | bool | Whether to use icons in the output (e.g. ⚠️ for warnings). |

## Customization

`easy-logger` is designed to be highly customizable. Here are some examples of how you can customize the output of your logs:

### Customize the Template

You can customize the template by passing a string to the `template` attribute of the `FormatterConfig` class. The template supports the following placeholders:

| Placeholder | Description |
| --- | --- |
| `{time}` | The current time in the format specified by the `date_format` attribute. |
| `{name}` | The name of the logger. |
| `{filename}` | The name of the file where the log message was generated. |
| `{lineno}` | The line number where the log message was generated. |
| `{level}` | The log level as a string. |
| `{level_icon}` | The log level as an icon. |
| `{message}` | The log message. |
| `{context}` | The context fields for the log message. |

Here's an example of how to customize the template:

```python
from easy_logging import FormatterConfig

config = FormatterConfig(
    template="[{time}] {level_icon} {level} | {message}",
)
```

### Customize the Date Format

You can customize the date format by passing a string to the `date_format` attribute of the `FormatterConfig` class. Here's an example of how to customize the date format:

```python
from easy_logging import FormatterConfig

config = FormatterConfig(
    date_format="%H:%M:%S",
)
```

### Customize the Colors

You can customize the colors by passing a `Theme` object to the `theme` attribute of the `EasyFormatter` class. Here's an example of how to customize the colors:

```python
from easy_logging import EasyFormatter, Theme

theme = Theme(
    level_colors={
        logging.DEBUG: Ansi.CYAN,
        logging.INFO: Ansi.GREEN,
        logging.WARNING: Ansi.YELLOW,
        logging.ERROR: Ansi.RED,
        logging.CRITICAL: Ansi.MAGENTA,
    },
)
formatter = EasyFormatter(theme=theme)
```

The `Theme` class has the following attributes:

| Attribute | Type | Description |
| --- | --- | --- |
| `default_color` | Ansi | The default color for log messages. |
| `level_colors` | dict[int, Ansi] | A dictionary mapping log levels to colors. |

The `Ansi` class has the following attributes:

| Attribute | Type | Description |
| --- | --- | --- |
| `RESET` | str | The reset code for ANSI escape sequences. |
| `BOLD` | str | The bold code for ANSI escape sequences. |
| `DIM` | str | The dim code for ANSI escape sequences. |
| `RED` | str | The red code for ANSI escape sequences. |
| `GREEN` | str | The green code for ANSI escape sequences. |
| `YELLOW` | str | The yellow code for ANSI escape sequences. |
| `BLUE` | str | The blue code for ANSI escape sequences. |
| `MAGENTA` | str | The magenta code for ANSI escape sequences. |
| `CYAN` | str | The cyan code for ANSI escape sequences. |
| `WHITE` | str | The white code for ANSI escape sequences. |

## License

`easy-logger` is licensed under the GNU General Public License v3.0. See the [LICENSE](LICENSE) file for more information.
