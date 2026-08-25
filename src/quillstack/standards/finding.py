"""What a check has to say about a package."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class Status(StrEnum):
    """Whether something is wrong, worth a look, or fine."""

    FAILED = "failed"
    WARNING = "warning"
    PASSED = "passed"


@dataclass(frozen=True)
class Finding:
    """One thing a check noticed.

    ``remedy`` is what to do about it. A finding which says something is wrong and not what
    would be right is a complaint rather than a check.
    """

    check: str
    status: Status
    message: str
    remedy: str = ""

    @classmethod
    def failed(cls, check: str, message: str, remedy: str = "") -> Finding:
        return cls(check, Status.FAILED, message, remedy)

    @classmethod
    def warning(cls, check: str, message: str, remedy: str = "") -> Finding:
        return cls(check, Status.WARNING, message, remedy)

    @classmethod
    def passed(cls, check: str, message: str) -> Finding:
        return cls(check, Status.PASSED, message)
