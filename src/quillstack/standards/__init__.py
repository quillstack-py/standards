"""Checks a Quillstack package against the shape every one of them takes.

The rules are not here. They are in ``rules.json``, which is one file shared with every other
language's checker, so a rule cannot mean one thing in Python and another in PHP.
"""

from quillstack.standards.finding import Finding
from quillstack.standards.package import Package
from quillstack.standards.standard import Standard

__all__ = ["Finding", "Package", "Standard"]
