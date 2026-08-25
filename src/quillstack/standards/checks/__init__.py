"""The checks themselves.

Each reads what it needs from the rules file rather than deciding anything of its own, so
changing a rule is changing the file rather than changing a checker.
"""

from quillstack.standards.checks.rendering import Rendering

from quillstack.standards.checks.badges import Badges
from quillstack.standards.checks.check import Check
from quillstack.standards.checks.readme_sections import ReadmeSections

__all__ = ["Badges", "Check", "ReadmeSections", "Rendering"]
