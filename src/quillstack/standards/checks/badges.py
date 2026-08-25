"""The badges, and whether they are all there."""

from __future__ import annotations

import re
from typing import ClassVar

from quillstack.standards.finding import Finding
from quillstack.standards.package import Package

BADGE = re.compile(r"\[!\[[^\]]*\]\(([^)]+)\)\]\(([^)]+)\)")


class Badges:
    """A row of badges says at a glance what a package's state is.

    Which ones are required is in the rules file. What each looks like is not, because the
    services differ by ecosystem — a PHP package points at Packagist and a Python one at PyPI —
    so the rule names the badge and the checker knows where its own ecosystem keeps it.
    """

    # The rule names a badge; where that ecosystem keeps it is this checker's business. A PHP
    # package points at Packagist and a Python one at PyPI, and the list of which badges are
    # required is the same file for both.
    KNOWN: ClassVar[dict[str, tuple[str, ...]]] = {
        "tests": ("actions/workflows",),
        "version": ("pypi/v",),
        "downloads": ("pypi/dm", "pypi/dd", "pepy.tech"),
        "language-version": ("pypi/pyversions",),
        "styleci": ("styleci",),
        "codefactor": ("codefactor",),
        "sonar-quality-gate": ("alert_status",),
        "sonar-coverage": ("metric=coverage",),
        "sonar-maintainability": ("sqale_rating",),
        "sonar-reliability": ("reliability_rating",),
        "sonar-security": ("security_rating",),
        "license": ("pypi/l", "img.shields.io/badge/license"),
    }

    def __init__(self, required: list[str], must_render: bool = True) -> None:
        self.required = required
        self.must_render = must_render

    def name(self) -> str:
        return "badges"

    def needs_network(self) -> bool:
        return False

    def run(self, package: Package) -> list[Finding]:
        if not package.has("README.md"):
            return [Finding.failed(self.name(), "There is no README.md.")]

        readme = package.read("README.md")
        urls = [image for image, _ in BADGE.findall(readme)]
        findings = []

        for badge in self.required:
            marks = self.KNOWN.get(badge, (badge,))

            if not any(any(mark in url for mark in marks) for url in urls):
                findings.append(
                    Finding.failed(
                        self.name(),
                        f"No `{badge}` badge.",
                        "The standard's badge block is in the skill, in the order it goes in.",
                    )
                )

        return findings or [Finding.passed(self.name(), f"{len(urls)} badges")]
