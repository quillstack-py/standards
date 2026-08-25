"""What every check looks like."""

from __future__ import annotations

from typing import Protocol

from quillstack.standards.finding import Finding
from quillstack.standards.package import Package


class Check(Protocol):
    """Something which has a name and an opinion about a package."""

    def name(self) -> str: ...

    def needs_network(self) -> bool: ...

    def run(self, package: Package) -> list[Finding]: ...
