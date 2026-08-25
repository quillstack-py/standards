"""The README says the same things in the same order in every package."""

from __future__ import annotations

import re
from typing import Any

from quillstack.standards.finding import Finding
from quillstack.standards.package import Package

SECTION = re.compile(r"^##\s+(.+)$", re.MULTILINE)
DEEPER = re.compile(r"^#{3,6}\s+(.+)$", re.MULTILINE)
TITLE = re.compile(r"^#\s+\S", re.MULTILINE)


class ReadmeSections:
    """A reader who has read one README knows where to look in the next.

    The sections and their order come from the rules file, so this holds the same opinion the
    PHP checker holds, for the same reason: it is the same list.
    """

    def __init__(
        self,
        sections: list[dict[str, Any]],
        ordered: bool = True,
        first_heading_is_title: bool = True,
    ) -> None:
        self.sections = sections
        self.ordered = ordered
        self.first_heading_is_title = first_heading_is_title

    def name(self) -> str:
        return "readme sections"

    def needs_network(self) -> bool:
        return False

    def run(self, package: Package) -> list[Finding]:
        if not package.has("README.md"):
            return [Finding.failed(self.name(), "There is no README.md.")]

        readme = package.read("README.md")
        found = [heading.strip() for heading in SECTION.findall(readme)]
        deeper = [heading.strip() for heading in DEEPER.findall(readme)]

        findings = self._missing(found, deeper, package.kind())
        findings += self._out_of_order(found)

        if self.first_heading_is_title and not TITLE.search(readme):
            findings.append(
                Finding.failed(self.name(), "The README does not open with a `# Title`.")
            )

        if findings:
            return findings

        return [
            Finding.passed(self.name(), f"{len(found)} sections, in the order the standard sets")
        ]

    def _missing(self, found: list[str], deeper: list[str], kind: str) -> list[Finding]:
        findings = []

        for section in self.sections:
            title = section["title"]

            if not section.get("required", False) or title in found:
                continue

            # A starter skeleton is not a library: there is nothing to add to a project which
            # is already the project, so `Installation` and `Usage` are one thing there.
            instead = (section.get("satisfiedBy") or {}).get(kind)

            if instead is not None and instead in found:
                continue

            findings.append(
                Finding.failed(
                    self.name(),
                    f"`{title}` is a sub-heading here, not a section.",
                    "The standard puts it at `##`. This README predates that.",
                )
                if title in deeper
                else Finding.failed(
                    self.name(),
                    f"No `## {title}` section.",
                    "Where a package has nothing to say under a heading, that is usually the "
                    "heading it needs most.",
                )
            )

        return findings

    def _out_of_order(self, found: list[str]) -> list[Finding]:
        """The order is part of the standard.

        A reader looking for how to install something should not have to find out where this
        package decided to put it.
        """
        if not self.ordered:
            return []

        expected = [section["title"] for section in self.sections]
        positions = {heading: expected.index(heading) for heading in found if heading in expected}

        if list(positions) == sorted(positions, key=lambda heading: positions[heading]):
            return []

        return [
            Finding.failed(
                self.name(),
                "The sections are not in the order the standard sets: "
                + " → ".join(positions),
                "Expected: "
                + " → ".join(sorted(positions, key=lambda heading: positions[heading])),
            )
        ]
