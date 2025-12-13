"""Command line utilities for managing OpenReward environments."""
from __future__ import annotations

import argparse
import re
from dataclasses import dataclass, field
from importlib import resources
from pathlib import Path
from string import Template
from typing import Callable, Mapping


@dataclass(frozen=True)
class TemplateFiles:
    """Collection of scaffold files for an environment."""

    dockerfile: str
    server_py: str
    extra_files: Mapping[str, str] = field(default_factory=dict)


def _pascal_case(name: str) -> str:
    parts = re.split(r"[^0-9a-zA-Z]+", name)
    cleaned = "".join(part.capitalize() for part in parts if part)
    if not cleaned:
        cleaned = "Environment"
    if cleaned[0].isdigit():
        cleaned = f"Env{cleaned}"
    return cleaned


def _load_template_file(template_name: str, filename: str) -> str:
    package = f"openreward.templates.{template_name}"
    file = resources.files(package).joinpath(filename)
    return file.read_text(encoding="utf-8")


def _basic_template(env_name: str) -> TemplateFiles:
    class_name = _pascal_case(env_name)
    dockerfile = _load_template_file("basic", "Dockerfile")
    server_template = Template(_load_template_file("basic", "server.py.tmpl"))
    server_py = server_template.substitute(CLASS_NAME=class_name)
    extra_files = {
        "requirements.txt": _load_template_file("basic", "requirements.txt"),
    }
    return TemplateFiles(dockerfile=dockerfile, server_py=server_py, extra_files=extra_files)


TemplateFactory = Callable[[str], TemplateFiles]


TEMPLATES: Mapping[str, TemplateFactory] = {
    "basic": _basic_template,
}


def _render_template(template_name: str, env_name: str) -> TemplateFiles:
    generator = TEMPLATES.get(template_name)
    if generator is None:
        raise ValueError(f"Unknown template '{template_name}'. Available templates: {', '.join(TEMPLATES)}")
    return generator(env_name)


def _write_file(path: Path, contents: str) -> None:
    if path.exists():
        raise FileExistsError(f"{path} already exists")
    path.write_text(contents, encoding="utf-8")


def command_init(environment: str, template: str) -> None:
    target_dir = Path.cwd() / environment
    target_dir.mkdir(parents=True, exist_ok=False)

    files = _render_template(template, environment)

    _write_file(target_dir / "Dockerfile", files.dockerfile)
    _write_file(target_dir / "server.py", files.server_py)
    for relative, contents in files.extra_files.items():
        _write_file(target_dir / relative, contents)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="orwd", description="OpenReward CLI utilities")
    subparsers = parser.add_subparsers(dest="command", required=True)

    init_parser = subparsers.add_parser(
        "init",
        help="Initialize a new environment template",
    )
    init_parser.add_argument("environment", help="Name of the environment to scaffold")
    init_parser.add_argument(
        "--template",
        default="basic",
        choices=sorted(TEMPLATES.keys()),
        help="Scaffold template to use (default: %(default)s)",
    )
    init_parser.set_defaults(func=lambda args: command_init(args.environment, args.template))

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        args.func(args)
    except FileExistsError as exc:
        parser.error(str(exc))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
