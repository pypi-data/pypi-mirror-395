from __future__ import annotations

import os

from wexample_helpers.classes.abstract_method import abstract_method


class AbstractDebug:
    def __init__(self) -> None:
        self.data = None
        self.cwd = os.getcwd()
        self.collect_data()

    @abstract_method
    def collect_data(self) -> None:
        """Collect debug data"""

    def execute(self) -> None:
        """Execute the debug operation"""
        self.print()

    def print(self, silent: bool = False) -> str:
        """Print debug data, or return it as text if return_text is True."""
        lines = self._render_data(self.data)
        text = "\n".join(lines)
        if not silent:
            print(text)
        return text

    def render(self) -> str:
        """Return the formatted debug output as a string without printing."""
        return "\n".join(self._render_data(self.data))

    def _format_attribute_value(self, name: str, value: dict, indent: str = "") -> str:
        """Format attribute value in a clean YAML-like format."""
        from wexample_helpers.const.colors import Colors

        visibility = self._get_attribute_visibility(name)
        value_type = value.get("type", "unknown")

        result = [
            f"{indent}  {Colors.BRIGHT}{name}:{Colors.RESET}",
            f"{indent}    {Colors.BLUE}type:{Colors.RESET} {value_type}",
            f"{indent}    {Colors.BLUE}visibility:{Colors.RESET} {visibility}",
        ]

        if value_type == "property":
            if value.get("has_getter"):
                result.append(f"{indent}    {Colors.BLUE}getter:{Colors.RESET} yes")
            if value.get("has_setter"):
                result.append(f"{indent}    {Colors.BLUE}setter:{Colors.RESET} yes")
            if value.get("has_deleter"):
                result.append(f"{indent}    {Colors.BLUE}deleter:{Colors.RESET} yes")
        else:
            result.append(
                f"{indent}    {Colors.BLUE}value:{Colors.RESET} {Colors.GREEN}{value.get('value', '')}{Colors.RESET}"
            )

        return "\n".join(result)

    def _format_attributes_header(self, indent: str = "") -> str:
        """Format attributes section header."""
        from wexample_helpers.const.colors import Colors

        return f"{indent}{Colors.BRIGHT}Instance attributes:{Colors.RESET}"

    def _format_class_name(self, name: str, module: str, indent: str = "") -> str:
        """Format class name with module. Use a distinct color for classes."""
        from wexample_helpers.const.colors import Colors

        result = f"{indent}{Colors.MAGENTA}→ {name}{Colors.RESET}"
        if module != "__main__":
            result += f" {Colors.GREEN}({module}){Colors.RESET}"
        return result

    def _format_file_path(self, path: str, line: int = None, indent: str = "") -> str:
        """Format file path with optional line number."""
        from wexample_helpers.const.colors import Colors
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        rel_path = self._get_relative_path(path)
        clickable_path = cli_make_clickable_path(path, short_title=rel_path)
        line_info = f":{line}" if line is not None else ""
        return f"{indent}    {Colors.YELLOW}File: {clickable_path}{line_info}{Colors.RESET}"

    def _format_instance_name(self, name: str, indent: str = "") -> str:
        """Format instance name with distinct class color."""
        from wexample_helpers.const.colors import Colors

        return f"{indent}{Colors.MAGENTA}Instance of {name}{Colors.RESET}"

    def _get_attribute_visibility(self, name: str) -> str:
        """Get attribute visibility based on name."""
        if name.startswith("__"):
            return "private"
        elif name.startswith("_"):
            return "protected"
        return "public"

    def _get_relative_path(self, path: str) -> str:
        """Convert absolute path to relative path if possible."""
        try:
            rel_path = os.path.relpath(path, self.cwd)
            if not rel_path.startswith("../"):
                return rel_path
        except ValueError:
            pass
        return path

    def _inline_data(self, data: dict) -> str:
        """Render a compact, one-line representation of a data node (used for dict keys)."""
        if not isinstance(data, dict):
            return str(data)
        # Prefer explicit value if present (already repr for primitives)
        if "value" in data:
            return data["value"]
        # Class/instance labels
        if data.get("type") == "class" and "name" in data:
            return data["name"]
        if "instance_of" in data:
            return data["instance_of"]
        # Fallback to type name
        t = data.get("type")
        return t if t is not None else str(data)

    def _render_data(self, data: dict, indent: str = "") -> list[str]:
        """Build the debug output as a list of lines (no printing)."""
        from wexample_helpers.const.colors import Colors

        lines: list[str] = []
        if not isinstance(data, dict):
            lines.append(
                f"{indent}{Colors.YELLOW}[Invalid data structure]{Colors.RESET}"
            )
            return lines

        data_type = data.get("type", "unknown")

        if data_type == "max_depth":
            lines.append(f"{indent}{Colors.YELLOW}[Max depth reached]{Colors.RESET}")
            return lines

        if data_type == "circular":
            lines.append(f"{indent}{Colors.YELLOW}[Circular reference]{Colors.RESET}")
            return lines

        if data_type == "class":
            lines.append(self._format_class_name(data["name"], data["module"], indent))
            if "source_file" in data:
                lines.append(self._format_file_path(data["source_file"], None, indent))

            if "attributes" in data:
                for name, value in data["attributes"].items():
                    lines.append(self._format_attribute_value(name, value, indent))

            if "bases" in data:
                for base in data["bases"]:
                    lines.extend(self._render_data(base, indent + "    "))
            return lines

        if "instance_of" in data:
            lines.append(self._format_instance_name(data["instance_of"], indent))
            if "dump_location" in data:
                location = data["dump_location"]
                lines.append(
                    self._format_file_path(location["file"], location["line"], indent)
                )

            if "class_data" in data:
                lines.extend(self._render_data(data["class_data"], indent + "  "))

            if "attributes" in data:
                lines.append(self._format_attributes_header(indent))
                for name, value in data["attributes"].items():
                    lines.append(self._format_attribute_value(name, value, indent))

        elif "value" in data:
            lines.append(
                f"{indent}{Colors.BLUE}{data['type']}{Colors.RESET}: {Colors.GREEN}{data['value']}{Colors.RESET}"
            )

        elif "elements" in data:
            lines.append(
                f"{indent}{Colors.BLUE}{data['type']}{Colors.RESET} ({len(data['elements'])} elements):"
            )
            for i, element in enumerate(data["elements"]):
                lines.append(f"{indent}  {Colors.BRIGHT}[{i}]{Colors.RESET} →")
                lines.extend(self._render_data(element, indent + "    "))

        elif "items" in data:
            lines.append(
                f"{indent}{Colors.BLUE}{data['type']}{Colors.RESET} ({len(data['items'])} elements):"
            )
            for item in data["items"]:
                key_inline = self._inline_data(item["key"])
                lines.append(f"{indent}  {Colors.BRIGHT}{key_inline}{Colors.RESET} →")
                lines.extend(self._render_data(item["value"], indent + "    "))

        return lines
