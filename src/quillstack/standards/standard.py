"""The standard: which checks there are, built from the rules file."""

from __future__ import annotations

from typing import Any

from quillstack.standards.checks import Badges, Check, Manifest, ReadmeSections, Rendering
from quillstack.standards.rules import at


class Standard:
    """Every check, configured from ``rules.json`` and from nothing else.

    A check which decided anything of its own would be a rule this file does not state, and the
    file is what the other checkers read.
    """

    def checks(self, online: bool = False) -> list[Check]:
        return [
            ReadmeSections(
                self._sections(),
                bool(at("readme.ordered", True)),
                bool(at("readme.firstHeadingIsTitle", True)),
            ),
            Badges(
                # The universal list, plus what only this ecosystem has. Python adds none: ruff
                # is a linter that runs in CI rather than a service with a shield.
                self._strings("badges.required") + self._strings("python.badges"),
                bool(at("badges.mustRender", True)),
            ),
            Rendering(bool(at("readme.rendering.noInlineBeforeLinkAcrossLineBreak", True))),
            Manifest(
                str(at("python.homepage", "")),
                self._strings("python.classifiers.required"),
                str(at("python.classifiers.perVersion", "")),
                self._strings("python.requiredFiles"),
            ),
        ]

    def _sections(self) -> list[dict[str, Any]]:
        sections = []

        for section in self._list("readme.sections"):
            if not isinstance(section, dict) or not isinstance(section.get("title"), str):
                continue

            sections.append(
                {
                    "title": section["title"],
                    "required": bool(section.get("required", False)),
                    "satisfiedBy": {
                        kind: title
                        for kind, title in (section.get("satisfiedBy") or {}).items()
                        if isinstance(kind, str) and isinstance(title, str)
                    },
                }
            )

        return sections

    def _list(self, path: str) -> list[Any]:
        value = at(path, [])

        return value if isinstance(value, list) else []

    def _strings(self, path: str) -> list[str]:
        return [value for value in self._list(path) if isinstance(value, str)]
