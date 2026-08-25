# Quillstack Standards

[![Tests](https://github.com/quillstack-py/standards/actions/workflows/tests.yml/badge.svg)](https://github.com/quillstack-py/standards/actions/workflows/tests.yml)
[![Latest Version](https://img.shields.io/pypi/v/quillstack-standards.svg)](https://pypi.org/project/quillstack-standards/)
[![Downloads](https://img.shields.io/pypi/dm/quillstack-standards.svg)](https://pypi.org/project/quillstack-standards/)
[![Python Version](https://img.shields.io/pypi/pyversions/quillstack-standards)](https://pypi.org/project/quillstack-standards/)
[![CodeFactor](https://www.codefactor.io/repository/github/quillstack-py/standards/badge)](https://www.codefactor.io/repository/github/quillstack-py/standards)
[![Quality Gate](https://sonarcloud.io/api/project_badges/measure?project=quillstack-py_standards&metric=alert_status)](https://sonarcloud.io/summary/new_code?id=quillstack-py_standards)
[![Coverage](https://sonarcloud.io/api/project_badges/measure?project=quillstack-py_standards&metric=coverage)](https://sonarcloud.io/summary/new_code?id=quillstack-py_standards)
[![Maintainability](https://sonarcloud.io/api/project_badges/measure?project=quillstack-py_standards&metric=sqale_rating)](https://sonarcloud.io/summary/new_code?id=quillstack-py_standards)
[![Reliability](https://sonarcloud.io/api/project_badges/measure?project=quillstack-py_standards&metric=reliability_rating)](https://sonarcloud.io/summary/new_code?id=quillstack-py_standards)
[![Security](https://sonarcloud.io/api/project_badges/measure?project=quillstack-py_standards&metric=security_rating)](https://sonarcloud.io/summary/new_code?id=quillstack-py_standards)
[![License](https://img.shields.io/pypi/l/quillstack-standards)](https://github.com/quillstack-py/standards/blob/main/LICENSE)

Checks a Quillstack package against the shape every one of them takes: the README, the badges,
the repository, the release.

## Why this exists

Quillstack is the same way of working in more than one language. What a package looks like — the
README sections and their order, the badges, where the homepage points, how a release is
verified and tagged — is meant to be the same whether the package is installed with `pip` or
with `composer`.

Which raises the obvious question: how does it stay the same?

**The rules are one file.** `rules.json` is shared with the PHP checker, so a rule cannot mean
one thing here and another there. Seven of its nine sections belong to no language in
particular; the rest name the ecosystem they are for.

**The checkers are not shared, and that is the point.** This is a thing you `pip install`. A
Python developer should not have to install PHP to check a Python package — that would make
Python the guest in its own ecosystem, which is the opposite of what the whole idea is for.

**And two implementations of one rule book drift**, which is the part that needs solving rather
than promising. See [Conformance](#conformance).

## Requirements

- Python 3.11 or newer

## Installation

```shell
pip install quillstack-standards
```

Or, without installing it anywhere:

```shell
uvx quillstack-standards
```

## Usage

Point it at a package:

```shell
$ quillstack-standards .
Checking quillstack-dotenv against the Quillstack standard

  ok   readme sections 8 sections, in the order the standard sets
  ok   badges          11 badges
  ok   rendering       nothing that reads correctly and renders wrongly

  3 passed, 0 to look at, 0 failed
```

It exits `1` where anything failed, so CI can use it without reading the output.

### What it checks

| Check | What it is about |
| --- | --- |
| `readme sections` | the sections the standard sets, present and in order |
| `badges` | the badge block, all of it |
| `rendering` | markdown which reads correctly and renders wrongly |
| `manifest` | the homepage, the classifiers, and the files a distribution ships |

Fewer than the PHP checker has, because this one is new. The rules for the rest are already in
`rules.json` — what is missing is the reading of them here, and a case in `conformance` will not
let that be forgotten quietly.

### A rule which bends for a skeleton

A starter project merges `Installation` and `Usage` into one `Getting started`, because there is
nothing to add to a project which already is the project. A `pyproject.toml` has no `type` field
the way a `composer.json` does, so a skeleton says so itself:

```toml
[tool.quillstack]
type = "project"
```

## Conformance

The rules cannot disagree — they are one file. **The readings of them can.** One checker decides
a section is missing where the other decides it is at the wrong level, and nobody notices until
the two disagree about somebody's package.

`conformance/` is what stops that: small packages, each with an `expected.json` saying which
checks must fail on it and how many times. Both checkers run all of them and must agree.

```json
{
    "about": "A required README section written at three hashes instead of two.",
    "scope": "universal",
    "checks": {"readme sections": {"failures": 1}}
}
```

The count is the contract and the wording is not, because the wording is each checker's own
business and **what** it objects to is the rule.

Two things were wrong with those cases until this package existed to run them. They carried only
`composer.json`, so nothing here could open them; and the badge list included StyleCI, which
checks PHP style and has nothing to say about Python. Neither would have been found by reading.

## Benchmark

Not measured. This reads a handful of files in a directory and runs some regular expressions
over them; it is quick enough that timing it would be measuring the process starting. Where a
package is slow to check, the checking is not why.

## Tests

```shell
uv run pytest
```

One of them fetches the canonical `rules.json` and compares it against the copy here, so the two
cannot part company quietly.

### Static analysis

```shell
uv run ruff check --no-cache
uv run mypy
```

`--no-cache` on purpose. A cached ruff result once said this package was clean while CI said it
was not, which is the same trick a stale PHPStan cache played on the PHP side the same week. A
local check that agrees with you may not have looked.

## The rest of Quillstack

This is one component of [Quillstack](https://quillstack.org), the same way of building APIs in
more than one language.

- [quillstack/standards](https://github.com/quillstack/standards) — the PHP checker, and where `rules.json` is kept
- [quillstack.org](https://quillstack.org) — the framework, and what exists of it in each language

## License

MIT — see [LICENSE](https://github.com/quillstack-py/standards/blob/main/LICENSE).
