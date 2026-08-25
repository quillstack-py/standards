"""The package being checked, and the manifest it keeps its name in."""

from __future__ import annotations

import tomllib
from functools import cached_property
from pathlib import Path
from typing import Any


class NotAPackageError(Exception):
    """Pointed at something which is not the root of a package."""


class Package:
    """A directory with a ``pyproject.toml`` in it.

    The PHP checker reads ``composer.json`` and this one reads ``pyproject.toml``; everything
    above that is the same rules file. That is the whole reason there are two checkers rather
    than one: a Python package is checked by something you ``pip install``, because asking for
    PHP to check Python would make Python the guest.
    """

    MANIFEST = "pyproject.toml"

    def __init__(self, path: str | Path) -> None:
        self.path = Path(path)

        if not (self.path / self.MANIFEST).is_file():
            raise NotAPackageError(
                f"No {self.MANIFEST} in `{self.path}`. Point this at the root of a package."
            )

    @cached_property
    def manifest(self) -> dict[str, Any]:
        with (self.path / self.MANIFEST).open("rb") as handle:
            return tomllib.load(handle)

    @property
    def project(self) -> dict[str, Any]:
        project = self.manifest.get("project")

        return project if isinstance(project, dict) else {}

    def name(self) -> str:
        """What the package is called, without the vendor part.

        PyPI has no vendor namespace the way Composer does, so a Quillstack package is called
        ``quillstack-<name>`` and this is the ``<name>``.
        """
        full = self.full_name()

        return full[len("quillstack-") :] if full.startswith("quillstack-") else full

    def full_name(self) -> str:
        name = self.project.get("name")

        return name if isinstance(name, str) else ""

    def kind(self) -> str:
        """``library`` unless the package says otherwise.

        The PHP manifest has a ``type``; a ``pyproject.toml`` does not, so a starter skeleton
        says so under Quillstack's own table rather than being guessed at.
        """
        tool = self.manifest.get("tool")
        quillstack = tool.get("quillstack") if isinstance(tool, dict) else None
        kind = quillstack.get("type") if isinstance(quillstack, dict) else None

        return kind if isinstance(kind, str) else "library"

    def has(self, file: str) -> bool:
        return (self.path / file).exists()

    def read(self, file: str) -> str:
        return (self.path / file).read_text(encoding="utf-8")
