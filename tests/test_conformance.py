"""The cases in ``conformance``, run against this checker.

There is one set of rules and a checker for every language Quillstack exists in. The rules
cannot disagree — they are a single file — but two implementations of them can. One checker
decides a section is missing where the other decides it is at the wrong level, and nobody
notices until they disagree about somebody's package.

These are the cases both checkers run. The count is the contract; the wording is not, because
the wording is each checker's own business.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

import pytest

from quillstack.standards import Package, Standard
from quillstack.standards.finding import Status

CASES = Path(__file__).parent.parent / "conformance"
SCOPES = {"universal", "python"}


def cases() -> list[tuple[str, dict[str, Any]]]:
    found = []

    for directory in sorted(CASES.iterdir()):
        expected = directory / "expected.json"

        if expected.is_file():
            found.append((directory.name, json.loads(expected.read_text(encoding="utf-8"))))

    return found


def applicable() -> list[tuple[str, dict[str, Any]]]:
    return [case for case in cases() if case[1].get("scope", "universal") in SCOPES]


def test_there_are_cases_to_run() -> None:
    """A conformance suite which found no cases would pass in silence, which is the one result
    it must never give.

    Only the cases this checker runs are kept here — the PHP-scoped ones stay in the PHP
    repository, because a Python package carrying `composer.json` and `phpstan.neon` around
    would be exactly the thing having two checkers is meant to avoid.
    """
    assert len(cases()) >= 3
    assert len(applicable()) == len(cases())


@pytest.mark.parametrize(("name", "expected"), applicable(), ids=lambda case: str(case))
def test_case_says_what_this_checker_says(name: str, expected: dict[str, Any]) -> None:
    package = Package(CASES / name)

    failures = {
        check.name(): len([f for f in check.run(package) if f.status is Status.FAILED])
        for check in Standard().checks()
    }

    for check, want in expected["checks"].items():
        if check not in failures:
            # A check this ecosystem does not have yet. Saying so is better than passing.
            pytest.skip(f"no `{check}` check here yet")

        assert failures[check] == want["failures"], f"{name}: {check}"


@pytest.mark.parametrize(("name", "expected"), cases(), ids=lambda case: str(case))
def test_every_case_says_what_it_is_for(name: str, expected: dict[str, Any]) -> None:
    assert expected.get("about")
    assert expected.get("checks")
