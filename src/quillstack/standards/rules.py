"""The rules, read from the file every checker reads.

``rules.json`` is a copy. The original lives in ``quillstack/standards`` — the PHP checker's
repository — because one of them has to be the original and that one was first. A test here
compares the copy against it, so the two cannot drift quietly.
"""

from __future__ import annotations

import json
from functools import cache
from pathlib import Path
from typing import Any

RULES = Path(__file__).with_name("rules.json")


@cache
def rules() -> dict[str, Any]:
    with RULES.open(encoding="utf-8") as handle:
        loaded: dict[str, Any] = json.load(handle)

    return loaded


def at(path: str, default: Any = None) -> Any:
    """A rule by its dotted path, as ``readme.sections`` or ``badges.mustRender``.

    The same paths the PHP checker asks for, because they are the same file.
    """
    value: Any = rules()

    for part in path.split("."):
        if not isinstance(value, dict) or part not in value:
            return default

        value = value[part]

    return value
