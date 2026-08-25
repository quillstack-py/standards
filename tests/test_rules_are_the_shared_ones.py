"""The rules file here is a copy, and a copy is a thing that drifts.

The original lives in ``quillstack/standards`` — the PHP checker's repository — because one of
them has to be the original and that one was first. This compares the copy against it, so the
two cannot part company quietly. Where the network is not there the test says so rather than
passing: a check that silently does nothing is worse than one that is red.
"""

from __future__ import annotations

import json
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import pytest

from quillstack.standards.rules import RULES

CANONICAL = "https://raw.githubusercontent.com/quillstack/standards/main/standard/rules.json"


def canonical() -> dict[str, Any] | None:
    try:
        with urllib.request.urlopen(CANONICAL, timeout=10) as response:
            loaded: dict[str, Any] = json.loads(response.read().decode("utf-8"))

            return loaded
    except (urllib.error.URLError, TimeoutError, json.JSONDecodeError):
        return None


def test_the_copy_is_the_original() -> None:
    upstream = canonical()

    if upstream is None:
        pytest.skip("the canonical rules could not be fetched")

    here = json.loads(Path(RULES).read_text(encoding="utf-8"))

    assert here == upstream, (
        "The rules here are not the rules every other checker reads. Copy "
        f"{CANONICAL} over {RULES}."
    )


def test_the_rules_say_which_scope_each_section_is() -> None:
    """A section without a scope is a rule nobody knows whether to apply."""
    here = json.loads(Path(RULES).read_text(encoding="utf-8"))

    for name, section in here.items():
        if isinstance(section, dict):
            assert section.get("scope") in {"universal", "php", "python"}, name
