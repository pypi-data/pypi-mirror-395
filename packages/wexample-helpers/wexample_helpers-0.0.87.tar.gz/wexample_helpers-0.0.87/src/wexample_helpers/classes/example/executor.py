from __future__ import annotations

from collections.abc import Iterable
from pathlib import Path
from typing import TYPE_CHECKING

from wexample_helpers.classes.field import public_field
from wexample_helpers.decorator.base_class import base_class
from wexample_helpers.helpers.module import (
    module_load_class_from_file_with_package_root,
)
from wexample_helpers.helpers.string import string_to_pascal_case
from wexample_helpers.mixin.with_entrypoint_path_mixin import WithEntrypointPathMixin
from wexample_helpers.service.mixins.registry_container_mixin import (
    RegistryContainerMixin,
)

if TYPE_CHECKING:
    from wexample_helpers.classes.example.example import Example


@base_class
class Executor(WithEntrypointPathMixin, RegistryContainerMixin):
    filters: tuple[str, ...] | None = public_field(
        default=None,
        description="Optional list of substrings to select which examples to run.",
    )

    def __attrs_post_init__(self) -> None:
        super().__attrs_post_init__()
        self._normalise_filters()
        examples_registry = self.get_registry("examples")
        examples_dir = Path(self.entrypoint_path).parent.resolve()
        from wexample_helpers.helpers.cli import cli_make_clickable_path

        package_name = examples_dir.name

        for path in self._iter_example_files(examples_dir):
            class_name = string_to_pascal_case(path.stem)
            try:
                example_class = module_load_class_from_file_with_package_root(
                    file_path=path,
                    class_name=class_name,
                    package_root=examples_dir,
                    package_name=package_name,
                )
            except Exception:
                self._print_log(
                    f'Bad example "{class_name}" in file: {cli_make_clickable_path(path)}'
                )
                continue

            if not isinstance(example_class, type) or not issubclass(
                example_class, self._get_example_class_type()
            ):
                self._print_log(
                    f'Bad example "{class_name}" in file: {cli_make_clickable_path(path)}'
                )
                continue

            key = self._build_example_key(path=path, root=examples_dir)

            examples_registry.register(
                key=key,
                item=example_class(path=path, executor=self),
            )

    def execute(self) -> None:
        examples_registry = self.get_registry("examples")
        matched = False
        for key, example in examples_registry.get_all().items():
            if not self._should_run_example(key, example):
                continue
            matched = True
            self._print_log(f"Running example: {key}")
            example.execute()

        if self.filters and not matched:
            filters = ", ".join(self.filters)
            self._print_log(f"No examples matched filters: {filters}")

    def _build_example_key(self, path: Path, root: Path) -> str:
        relative = path.relative_to(root).with_suffix("")
        return str(relative).replace("\\", "/")

    def _get_example_class_type(self) -> type[Example]:
        from wexample_helpers.classes.example.example import Example

        return Example

    def _iter_example_files(self, root: Path) -> list[Path]:
        files: list[Path] = []
        for path in sorted(root.rglob("*.py")):
            if not path.is_file():
                continue
            if path.name in {"__init__.py", "__main__.py"}:
                continue
            if path.name.startswith("_"):
                continue
            # avoid reprocessing files outside the root via symlinks
            try:
                path.relative_to(root)
            except ValueError:
                continue
            files.append(path)
        return files

    def _normalise_filters(self) -> None:
        raw_filters = self.filters

        if raw_filters is None or (
            isinstance(raw_filters, str) and not raw_filters.strip()
        ):
            self.filters = None
            self._filters_lower: tuple[str, ...] = ()
            return

        if isinstance(raw_filters, str):
            tokens: Iterable[str] = (raw_filters,)
        elif isinstance(raw_filters, Iterable):
            tokens = raw_filters
        else:
            tokens = (str(raw_filters),)

        cleaned = tuple(
            filter(
                None,
                (str(token).strip() for token in tokens),
            )
        )

        self.filters = cleaned or None
        self._filters_lower = tuple(f.lower() for f in cleaned) if cleaned else ()

    def _print_log(self, message: str) -> None:
        print(message)

    def _should_run_example(self, key: str, example: Example) -> bool:
        if not self.filters:
            return True
        key_lower = key.lower()
        class_name = example.__class__.__name__.lower()
        return any(
            token in key_lower or token in class_name for token in self._filters_lower
        )
