from __future__ import annotations

import re
from collections.abc import Callable


def string_append_missing_lines(lines: list[str], content: str) -> str:
    # Normalize content by removing trailing empty lines for consistent comparison
    content = string_remove_trailing_empty_lines(content)

    # Split the current content into lines
    current_lines = content.splitlines()

    # Determine the lines that need to be added (deduplicate to avoid adding same line multiple times)
    lines_to_add = []
    seen = set(current_lines)
    for line in lines:
        if line not in seen:
            lines_to_add.append(line)
            seen.add(line)

    if lines_to_add:
        # Ensure the content ends with a newline before appending new lines
        content = string_ensure_end_with_new_line(content)
        # Add the missing lines
        content += "\n".join(lines_to_add) + "\n"

    return content


def string_capitalize_first(text: str) -> str:
    """
    Capitalize only the first letter of the string (safe version).
    """
    return text[:1].upper() + text[1:] if text else text


def string_convert_case(text: str, to_format: str) -> str:
    """
    Convert text to any case format.

    :param text: The string to convert
    :param to_format: Target format - one of: 'snake', 'kebab', 'camel', 'pascal', 'constant', 'title', 'dot', 'path'
    :return: Converted string
    :raises ValueError: If to_format is not recognized
    """
    converters = string_convert_case_map()

    if to_format not in converters:
        valid_formats = ", ".join(converters.keys())
        raise ValueError(
            f"Invalid format '{to_format}'. Must be one of: {valid_formats}"
        )

    return converters[to_format](text)


def string_convert_case_map() -> dict[str, Callable[[str], str]]:
    return {
        "snake": string_to_snake_case,
        "kebab": string_to_kebab_case,
        "camel": string_to_camel_case,
        "pascal": string_to_pascal_case,
        "constant": string_to_constant_case,
        "title": string_to_title_case,
        "dot": string_to_dot_case,
        "path": string_to_path_case,
    }


def string_detect_case(text: str) -> str:
    """
    Detect the case format of a string.

    :param text: The string to analyze
    :return: One of: 'snake', 'kebab', 'camel', 'pascal', 'constant', 'title', 'dot', 'path', 'mixed', 'unknown'
    """
    if not text or not text.strip():
        return "unknown"

    text = text.strip()

    # Check for specific patterns
    if re.match(r"^[A-Z][A-Z0-9_]*$", text):
        return "constant"
    if re.match(r"^[a-z][a-z0-9]*(_[a-z0-9]+)*$", text):
        return "snake"
    if re.match(r"^[a-z][a-z0-9]*(-[a-z0-9]+)*$", text):
        return "kebab"
    if re.match(r"^[a-z][a-z0-9]*(\.[a-z0-9]+)*$", text):
        return "dot"
    if re.match(r"^[a-z][a-z0-9]*(/[a-z0-9]+)*$", text):
        return "path"
    if re.match(r"^[a-z][a-zA-Z0-9]*$", text) and re.search(r"[A-Z]", text):
        return "camel"
    if re.match(r"^[A-Z][a-zA-Z0-9]*$", text):
        return "pascal"
    if re.match(r"^[A-Z][a-z]+(\s[A-Z][a-z]+)*$", text):
        return "title"

    # Check for mixed separators
    separators = sum(
        [
            "_" in text,
            "-" in text,
            "." in text,
            "/" in text,
            bool(re.search(r"[a-z][A-Z]", text)),
        ]
    )

    if separators > 1:
        return "mixed"

    return "unknown"


def string_ensure_end_with_new_line(text: str) -> str:
    return text if text.endswith("\n") else text + "\n"


def string_generate_lorem_ipsum(length: int = 100) -> str:
    if length <= 0:
        return ""

    base = (
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit. "
        "Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. "
        "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. "
        "Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. "
        "Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
    )

    text = (base + " ") * ((length // (len(base) + 1)) + 1)

    cut = text[:length].rstrip()

    if (
        len(cut) == length
        and length < len(text)
        and not cut.endswith((" ", ".", ",", "!", "?", ";", ":"))
    ):
        last_space = cut.rfind(" ")
        if last_space > 0:
            cut = cut[:last_space]

    return cut.strip()


def string_is_camel_case(text: str) -> bool:
    """Check if text is in camelCase format."""
    return string_detect_case(text) == "camel"


def string_is_constant_case(text: str) -> bool:
    """Check if text is in CONSTANT_CASE format."""
    return string_detect_case(text) == "constant"


def string_is_dot_case(text: str) -> bool:
    """Check if text is in dot.case format."""
    return string_detect_case(text) == "dot"


def string_is_kebab_case(text: str) -> bool:
    """Check if text is in kebab-case format."""
    return string_detect_case(text) == "kebab"


def string_is_pascal_case(text: str) -> bool:
    """Check if text is in PascalCase format."""
    return string_detect_case(text) == "pascal"


def string_is_path_case(text: str) -> bool:
    """Check if text is in path/case format."""
    return string_detect_case(text) == "path"


def string_is_snake_case(text: str) -> bool:
    """Check if text is in snake_case format."""
    return string_detect_case(text) == "snake"


def string_is_title_case(text: str) -> bool:
    """Check if text is in Title Case format."""
    return string_detect_case(text) == "title"


def string_remove_prefix(string: str, prefix: str) -> str:
    """
    Remove a prefix from a string if it exists at the beginning.
    Uses regex to match the exact prefix at the start of the string.

    :param string: The string to process
    :param prefix: The prefix to remove
    :return: String with prefix removed if found at start
    """
    return re.sub(f"^{re.escape(prefix)}", "", string)


def string_remove_trailing_empty_lines(content: str) -> str:
    """
    Remove trailing empty lines from content while preserving the final newline if present.

    :param content: The string content to normalize
    :return: Content with trailing empty lines removed
    """
    if not content:
        return content

    lines = content.splitlines()
    # Remove trailing empty lines
    while lines and not lines[-1].strip():
        lines.pop()

    # Rejoin and preserve final newline if original had one
    result = "\n".join(lines)
    if result and content.endswith("\n"):
        result += "\n"

    return result


def string_render_boolean(boolean: bool) -> str:
    return "True" if boolean else "False"


def string_replace_params(text: str, params: dict) -> str:
    """
    Replace parameters in a text string with values from a dictionary.
    Each parameter in the text should be in the format %param_name%.
    Example:
        text = "Hello %name%, you are %age% years old"
        params = {"name": "John", "age": "30"}
        result = "Hello John, you are 30 years old"
    """
    result = text
    for key, value in params.items():
        result = result.replace(f"%{key}%", str(value))
    return result


def string_to_camel_case(text: str) -> str:
    """
    Convert text to camelCase (e.g. 'my_example_string' -> 'myExampleString').
    """
    words = _normalize(text)
    if not words:
        return ""
    return words[0] + "".join(w.capitalize() for w in words[1:])


def string_to_constant_case(text: str) -> str:
    """
    Convert text to CONSTANT_CASE (e.g. "MyClassName" -> "MY_CLASS_NAME").
    """
    return "_".join(_normalize(text)).upper()


def string_to_dot_case(text: str) -> str:
    """
    Convert text to dot.case (e.g. "MyClassName" -> "my.class.name").
    Useful for configuration keys and namespaces.
    """
    return ".".join(_normalize(text))


def string_to_kebab_case(text: str) -> str:
    """
    Convert text to kebab-case (e.g. "MyClassName" -> "my-class-name").
    """
    return "-".join(_normalize(text))


def string_to_pascal_case(text: str) -> str:
    """
    Convert text to PascalCase (ClassCase), e.g. 'my_example_string' -> 'MyExampleString'.
    """
    return "".join(w.capitalize() for w in _normalize(text))


def string_to_path_case(text: str) -> str:
    """
    Convert text to path/case (e.g. "MyClassName" -> "my/class/name").
    Useful for file paths and URL segments.
    """
    return "/".join(_normalize(text))


def string_to_snake_case(text: str) -> str:
    """
    Convert text to snake_case (e.g. "MyClassName" -> "my_class_name").
    """
    return "_".join(_normalize(text))


def string_to_title_case(text: str) -> str:
    """
    Convert text to Title Case (capitalize first letter of each word).
    """
    return " ".join(w.capitalize() for w in _normalize(text))


def string_truncate(text: str, limit: int) -> str:
    if len(text) > limit:
        return text[: limit - 3] + "..."
    return text


def _normalize(value: str) -> list[str]:
    """
    Convert any string into a normalized list of lowercase words.
    Handles:
    - camelCase / PascalCase
    - snake_case
    - kebab-case
    - dotted.case
    - path/case
    - mixed separators
    """

    if not value:
        return []

    # Trim whitespace
    value = value.strip()

    # Replace all non-alphanumeric separators with space
    value = re.sub(r"[^A-Za-z0-9]+", " ", value)

    # Split camelCase / PascalCase
    value = re.sub(r"([a-z0-9])([A-Z])", r"\1 \2", value)

    # Split multiple caps like "JSONParser" → "JSON Parser"
    value = re.sub(r"([A-Z]+)([A-Z][a-z])", r"\1 \2", value)

    # Normalize spaces
    parts = value.lower().split()

    # Remove empty segments
    return [p for p in parts if p]
