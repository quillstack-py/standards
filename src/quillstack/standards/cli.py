"""``quillstack-standards check`` — what a package looks like against the standard."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from quillstack.standards.finding import Finding, Status
from quillstack.standards.package import NotAPackageError, Package
from quillstack.standards.standard import Standard

MARK = {Status.PASSED: "ok  ", Status.WARNING: "~   ", Status.FAILED: "FAIL"}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="quillstack-standards",
        description="Checks a Quillstack package against the shape every one of them takes.",
    )
    parser.add_argument("path", nargs="?", default=".", help="the root of the package")
    parser.add_argument(
        "--online",
        action="store_true",
        help="also ask the services whether the badges answer",
    )

    arguments = parser.parse_args(argv)

    try:
        package = Package(Path(arguments.path))
    except NotAPackageError as error:
        print(error, file=sys.stderr)

        return 2

    print(f"Checking {package.full_name()} against the Quillstack standard\n")

    findings: list[Finding] = []

    for check in Standard().checks(arguments.online):
        findings.extend(check.run(package))

    for finding in findings:
        print(f"  {MARK[finding.status]} {finding.check:<16}{finding.message}")

        if finding.remedy:
            print(f"       {'':<16}{finding.remedy}")

    failed = sum(1 for finding in findings if finding.status is Status.FAILED)
    warned = sum(1 for finding in findings if finding.status is Status.WARNING)
    passed = len(findings) - failed - warned

    print(f"\n  {passed} passed, {warned} to look at, {failed} failed")

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
