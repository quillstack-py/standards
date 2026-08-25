"""Markdown which reads correctly and renders wrongly."""

from __future__ import annotations

import re

from quillstack.standards.finding import Finding
from quillstack.standards.package import Package

FENCE = re.compile(r"^\s*```")
ENDS_INLINE = re.compile(r"(\*\*[^*]+\*\*|`[^`]+`|\*[^*]+\*)\s*$")
STARTS_LINK = re.compile(r"^\s*\[[^\]]+\]\(")


class Rendering:
    """A README here is wrapped at a hundred characters, so a sentence breaks where it reaches
    the margin.

    Where an inline element lands at the end of a line and a link starts the next, the renderer
    drops the space between them: ``**with**`` and ``[a link]`` come out as ``witha link``. A
    plain word before a link is fine and bold before plain text is fine — it is the two together
    across the break, which is exactly what nobody spots while writing and everybody spots while
    reading.
    """

    def __init__(self, enabled: bool = True) -> None:
        self.enabled = enabled

    def name(self) -> str:
        return "rendering"

    def needs_network(self) -> bool:
        return False

    def run(self, package: Package) -> list[Finding]:
        if not self.enabled:
            return [Finding.passed(self.name(), "not checked")]

        if not package.has("README.md"):
            return [Finding.failed(self.name(), "There is no README.md.")]

        lines = package.read("README.md").splitlines()
        findings = []
        fenced = False

        for number, line in enumerate(lines[:-1], start=1):
            if FENCE.match(line):
                fenced = not fenced

            # Inside a fence the renderer is not reading it as prose, so neither is this.
            if fenced:
                continue

            if ENDS_INLINE.search(line) and STARTS_LINK.match(lines[number]):
                findings.append(
                    Finding.failed(
                        self.name(),
                        f"Line {number} ends with an inline element and line {number + 1} "
                        "starts with a link.",
                        "The space between them disappears when it renders. Move the link up, "
                        "or break the line somewhere else.",
                    )
                )

        return findings or [
            Finding.passed(self.name(), "nothing that reads correctly and renders wrongly")
        ]
