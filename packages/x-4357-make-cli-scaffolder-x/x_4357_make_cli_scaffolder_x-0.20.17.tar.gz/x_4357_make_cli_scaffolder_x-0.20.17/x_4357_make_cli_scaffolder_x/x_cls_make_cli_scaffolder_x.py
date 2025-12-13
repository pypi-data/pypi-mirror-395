"""Scaffold a disciplined CLI project skeleton."""

from __future__ import annotations

import argparse
import json
import logging
import sys
from collections.abc import Iterable, Mapping, Sequence
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from textwrap import dedent
from typing import Final, TypedDict, cast

LOGGER = logging.getLogger(__name__)

SCHEMA_VERSION: Final[str] = "x_make_cli_scaffolder_x.run/1.0"


class RunResult(TypedDict):
    status: str
    schema_version: str
    root_path: str
    created_files: list[str]


@dataclass(slots=True)
class _CliArgs:
    project_name: str
    target_dir: str
    description: str
    author: str | None
    version: str
    python_version: str
    package_name: str | None
    script_name: str | None
    include_tests: bool
    include_license: bool
    emit_json: bool


def _slugify(value: str, *, separator: str) -> str:
    lowered = value.strip().lower()
    if not lowered:
        return "app"
    parts: list[str] = []
    pending_sep = False
    for char in lowered:
        if char.isalnum():
            parts.append(char)
            pending_sep = False
        elif not pending_sep and parts:
            parts.append(separator)
            pending_sep = True
    cleaned = "".join(parts).strip(separator)
    if not cleaned:
        cleaned = "app"
    if cleaned[0].isdigit():
        cleaned = f"app{separator}{cleaned}"
    return cleaned


def _normalise_package_name(value: str) -> str:
    return _slugify(value, separator="_")


def _normalise_script_name(value: str) -> str:
    return _slugify(value, separator="-")


@dataclass(slots=True)
class ProjectConfig:
    project_name: str
    package_name: str
    description: str = ""
    version: str = "0.1.0"
    author: str | None = None
    python_version: str = "3.11"
    include_tests: bool = True
    include_license: bool = True
    script_name: str | None = None

    @classmethod
    def from_mapping(cls, payload: Mapping[str, object]) -> ProjectConfig:
        project_name = _require_str(payload, "project_name")
        package_raw = payload.get("package_name")
        package_name = _normalise_package_name(
            project_name if package_raw is None else str(package_raw)
        )
        description = str(payload.get("description", "") or "")
        version = str(payload.get("version", "0.1.0") or "0.1.0")
        author_value = payload.get("author")
        author = (
            str(author_value)
            if author_value is not None and author_value != ""
            else None
        )
        python_version = str(payload.get("python_version", "3.11") or "3.11")
        include_tests = bool(payload.get("include_tests", True))
        include_license = bool(payload.get("include_license", True))
        script_raw = payload.get("script_name")
        script_name = (
            _normalise_script_name(str(script_raw)) if script_raw is not None else None
        )
        return cls(
            project_name=project_name,
            package_name=package_name,
            description=description,
            version=version,
            author=author,
            python_version=python_version,
            include_tests=include_tests,
            include_license=include_license,
            script_name=script_name,
        )

    @property
    def resolved_script_name(self) -> str:
        if self.script_name:
            return self.script_name
        return _normalise_script_name(self.project_name)

    @property
    def console_entrypoint(self) -> str:
        return f"{self.package_name}.cli:main"


@dataclass(slots=True)
class ScaffoldResult:
    root_path: Path
    created_files: tuple[Path, ...]

    def to_dict(self) -> dict[str, object]:
        return {
            "root_path": str(self.root_path),
            "created_files": [str(path) for path in self.created_files],
        }


class CliScaffolder:
    def __init__(self, *, overwrite: bool = False) -> None:
        self._overwrite = overwrite

    def scaffold(self, target_dir: Path, config: ProjectConfig) -> ScaffoldResult:
        root_path = target_dir / config.project_name
        if root_path.exists() and not self._overwrite and any(root_path.iterdir()):
            message = f"Directory '{root_path}' is not empty"
            raise FileExistsError(message)
        root_path.mkdir(parents=True, exist_ok=True)
        created: list[Path] = []
        for relative_path, contents in self._render_file_map(config):
            file_path = root_path / relative_path
            file_path.parent.mkdir(parents=True, exist_ok=True)
            if file_path.exists() and not self._overwrite:
                message = f"File '{file_path}' already exists"
                raise FileExistsError(message)
            file_path.write_text(contents, encoding="utf-8")
            created.append(file_path)
        if config.include_license:
            license_path = root_path / "LICENSE"
            if license_path.exists() and not self._overwrite:
                message = f"File '{license_path}' already exists"
                raise FileExistsError(message)
            license_path.write_text(_render_mit_license(config), encoding="utf-8")
            created.append(license_path)
        LOGGER.info("Scaffolded CLI project at %s", root_path)
        return ScaffoldResult(root_path=root_path, created_files=tuple(created))

    def _render_file_map(self, config: ProjectConfig) -> Iterable[tuple[str, str]]:
        yield "README.md", _render_project_readme(config)
        yield "pyproject.toml", _render_pyproject(config)
        yield ".gitignore", _render_gitignore()
        package_root = f"src/{config.package_name}"
        yield f"{package_root}/__init__.py", "__all__ = ['main']\n"
        yield f"{package_root}/cli.py", _render_cli_module(config)
        yield f"{package_root}/__main__.py", _render_dunder_main()
        yield f"{package_root}/py.typed", ""
        if config.include_tests:
            yield "tests/__init__.py", ""
            yield "tests/test_cli.py", _render_pytest_module(config)


def _render_project_readme(config: ProjectConfig) -> str:
    usage = config.resolved_script_name
    return (
        f"# {config.project_name}\n\n"
        f"{config.description or 'Generated by x_make_cli_scaffolder_x.'}\n\n"
        "## Usage\n"
        "```bash\n"
        f"{usage} --help\n"
        "```\n"
    )


def _render_pyproject(config: ProjectConfig) -> str:
    author_block = ""
    if config.author:
        author_block = (
            "    authors = [\n" f'        {{ name = "{config.author}" }}\n' "    ]\n"
        )
    script_name = config.resolved_script_name
    return (
        "[build-system]\n"
        'requires = ["setuptools>=68", "wheel"]\n'
        'build-backend = "setuptools.build_meta"\n\n'
        "[project]\n"
        f'name = "{script_name}"\n'
        f'version = "{config.version}"\n'
        f'description = "{config.description}"\n'
        'readme = "README.md"\n'
        f'requires-python = ">={config.python_version}"\n'
        f"{author_block}"
        "\n"
        "[project.scripts]\n"
        f'{script_name} = "{config.console_entrypoint}"\n'
    )


def _render_gitignore() -> str:
    return (
        "__pycache__/\n"
        "*.py[cod]\n"
        "*.pyo\n"
        "*.tmp\n"
        ".venv/\n"
        "venv/\n"
        "build/\n"
        "dist/\n"
    )


def _render_cli_module(config: ProjectConfig) -> str:
    description = config.description or "CLI application entrypoint"
    return (
        "from __future__ import annotations\n\n"
        "import argparse\n\n"
        f'DESCRIPTION = "{description}"\n\n'
        "def _build_parser() -> argparse.ArgumentParser:\n"
        "    parser = argparse.ArgumentParser(description=DESCRIPTION)\n"
        "    parser.add_argument('--name', default='world', help='Name to greet.')\n"
        "    return parser\n\n"
        "def main(argv: list[str] | None = None) -> int:\n"
        "    parser = _build_parser()\n"
        "    args = parser.parse_args(argv)\n"
        "    print(f'Hello, {args.name}!')\n"
        "    return 0\n"
    )


def _render_dunder_main() -> str:
    return (
        "from __future__ import annotations\n\n"
        "from .cli import main\n\n"
        "if __name__ == '__main__':\n"
        "    raise SystemExit(main())\n"
    )


def _render_pytest_module(config: ProjectConfig) -> str:
    package = config.package_name
    return dedent(
        f"""
        from __future__ import annotations

        import importlib
        import runpy
        import pytest


        @pytest.mark.parametrize(
            ("argv", "expected"),
            [
                (None, "Hello, world!"),
                (["--name", "Tester"], "Hello, Tester!"),
            ],
        )
        def test_cli_output(
            argv: list[str] | None,
            expected: str,
            capsys: pytest.CaptureFixture[str],
        ) -> None:
            module = importlib.import_module("{package}.cli")
            result = module.main(argv)
            captured = capsys.readouterr()
            assert result == 0
            assert expected in captured.out


        def test_module_executes_via_python_m() -> None:
            result = runpy.run_module(
                "{package}",
                run_name="__main__",
                alter_sys=True,
            )
            assert isinstance(result, dict)
        """
    ).strip()


def _render_mit_license(config: ProjectConfig) -> str:
    year = datetime.now(UTC).year
    holder = config.author or "Author"
    body = f"""
    MIT License

    Copyright (c) {year} {holder}

    Permission is hereby granted, free of charge, to any person obtaining a copy
    of this software and associated documentation files (the "Software"), to deal
    in the Software without restriction, including without limitation the rights
    to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
    copies of the Software, and to permit persons to whom the Software is
    furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all
    copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
    IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
    FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
    AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
    LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
    OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
    SOFTWARE.
    """
    return dedent(body).lstrip()


def _require_str(payload: Mapping[str, object], key: str) -> str:
    value = payload.get(key)
    if not isinstance(value, str) or not value.strip():
        message = f"Parameter '{key}' must be a non-empty string"
        raise ValueError(message)
    return value.strip()


def _optional_str(value: object) -> str | None:
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def run(payload: Mapping[str, object]) -> RunResult:
    parameters_obj = payload.get("parameters")
    if not isinstance(parameters_obj, Mapping):
        message = "Payload parameters must be a mapping"
        raise TypeError(message)
    parameters = cast("Mapping[str, object]", parameters_obj)
    target_dir_obj = parameters.get("target_dir", ".")
    target_dir = Path(str(target_dir_obj))
    config = ProjectConfig.from_mapping(parameters)
    scaffolder = CliScaffolder()
    result = scaffolder.scaffold(target_dir.resolve(), config)
    output: RunResult = {
        "status": "success",
        "schema_version": SCHEMA_VERSION,
        "root_path": str(result.root_path),
        "created_files": [str(path) for path in result.created_files],
    }
    return output


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate a CLI project scaffold")
    parser.add_argument("--project-name", required=True, help="Project directory name")
    parser.add_argument(
        "--target-dir", default=".", help="Directory where the project will be created"
    )
    parser.add_argument("--description", default="", help="Project description")
    parser.add_argument(
        "--author", default=None, help="Author name for README and LICENSE"
    )
    parser.add_argument(
        "--version", default="0.1.0", help="Initial version for pyproject.toml"
    )
    parser.add_argument(
        "--python-version", default="3.11", help="Minimum Python version"
    )
    parser.add_argument(
        "--package-name", default=None, help="Override the generated package name"
    )
    parser.add_argument(
        "--script-name", default=None, help="Override the console script name"
    )
    parser.add_argument("--no-tests", action="store_true", help="Skip pytest scaffold")
    parser.add_argument(
        "--no-license", action="store_true", help="Skip MIT license stub"
    )
    parser.add_argument(
        "--json", action="store_true", help="Emit JSON summary instead of text"
    )
    namespace = parser.parse_args(list(argv) if argv is not None else None)
    namespace_dict = cast("dict[str, object]", vars(namespace))
    args = _CliArgs(
        project_name=str(namespace_dict["project_name"]),
        target_dir=str(namespace_dict["target_dir"]),
        description=str(namespace_dict.get("description", "")),
        author=_optional_str(namespace_dict.get("author")),
        version=str(namespace_dict.get("version", "0.1.0")),
        python_version=str(namespace_dict.get("python_version", "3.11")),
        package_name=_optional_str(namespace_dict.get("package_name")),
        script_name=_optional_str(namespace_dict.get("script_name")),
        include_tests=not bool(namespace_dict.get("no_tests", False)),
        include_license=not bool(namespace_dict.get("no_license", False)),
        emit_json=bool(namespace_dict.get("json", False)),
    )

    config_payload: dict[str, object] = {
        "project_name": args.project_name,
        "package_name": args.package_name,
        "description": args.description,
        "author": args.author,
        "version": args.version,
        "python_version": args.python_version,
        "include_tests": args.include_tests,
        "include_license": args.include_license,
        "script_name": args.script_name,
    }
    config = ProjectConfig.from_mapping(config_payload)
    result = CliScaffolder().scaffold(Path(args.target_dir).resolve(), config)
    if args.emit_json:
        json_payload: dict[str, object] = {"status": "success"}
        json_payload.update(result.to_dict())
        json.dump(json_payload, sys.stdout, indent=2)
        sys.stdout.write("\n")
    else:
        print(f"Scaffold created at {result.root_path}")
        for created in result.created_files:
            print(f" - {created.relative_to(result.root_path)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
