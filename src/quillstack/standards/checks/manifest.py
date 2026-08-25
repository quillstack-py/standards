"""What the distribution says about itself."""

from __future__ import annotations

from typing import Any

from quillstack.standards.finding import Finding
from quillstack.standards.package import Package


class Manifest:
    """The parts of ``pyproject.toml`` a reader and an installer both rely on.

    The classifiers are here because the first release of this package had none, and its
    ``python`` badge rendered the word ``missing``: shields.io reads the classifiers rather than
    ``requires-python``. Nothing said to have any, so nothing objected — which is what a rule is
    for.
    """

    def __init__(
        self,
        homepage: str,
        classifiers: list[str],
        per_version: str,
        required_files: list[str],
    ) -> None:
        self.homepage = homepage
        self.classifiers = classifiers
        self.per_version = per_version
        self.required_files = required_files

    def name(self) -> str:
        return "manifest"

    def needs_network(self) -> bool:
        return False

    def run(self, package: Package) -> list[Finding]:
        project = package.project
        findings = self._homepage(project, package.name())
        findings += self._classifiers(project)
        findings += self._files(package)

        return findings or [
            Finding.passed(self.name(), "homepage, classifiers and files all present")
        ]

    def _homepage(self, project: dict[str, Any], name: str) -> list[Finding]:
        urls = project.get("urls")
        homepage = urls.get("Homepage") if isinstance(urls, dict) else None
        wanted = self.homepage.replace("{name}", name)

        if homepage == wanted:
            return []

        return [
            Finding.failed(
                self.name(),
                f"The homepage is `{homepage}`.",
                f"It points at the package's own documentation page: `{wanted}`.",
            )
        ]

    def _classifiers(self, project: dict[str, Any]) -> list[Finding]:
        declared = project.get("classifiers")
        declared = declared if isinstance(declared, list) else []
        findings = []

        for classifier in self.classifiers:
            if classifier not in declared:
                findings.append(
                    Finding.failed(
                        self.name(),
                        f"No `{classifier}` classifier.",
                        "shields.io reads the classifiers rather than `requires-python`, so a "
                        "distribution without them renders a `python` badge saying `missing`.",
                    )
                )

        marker = self.per_version.replace("{version}", "")

        if not any(c.startswith(marker) and c != marker.rstrip() for c in declared):
            findings.append(
                Finding.failed(
                    self.name(),
                    "No version classifiers.",
                    "One per version actually supported, as "
                    f"`{self.per_version.replace('{version}', '3.12')}`.",
                )
            )

        return findings

    def _files(self, package: Package) -> list[Finding]:
        findings = []

        for file in self.required_files:
            if package.has(file) or package.has(f"src/quillstack/{package.name()}/{file}"):
                continue

            findings.append(Finding.failed(self.name(), f"There is no `{file}`."))

        return findings
