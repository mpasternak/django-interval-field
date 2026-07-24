# django-pgsql-interval-field

[![Tests](https://github.com/mpasternak/django-interval-field/actions/workflows/tests.yml/badge.svg)](https://github.com/mpasternak/django-interval-field/actions/workflows/tests.yml)
[![PyPI](https://img.shields.io/pypi/v/django-pgsql-interval-field.svg)](https://pypi.org/project/django-pgsql-interval-field/)
![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)
![Django](https://img.shields.io/badge/django-5.2%20%7C%206.0-blue)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

An `INTERVAL` model field for Django, backed by PostgreSQL's native `INTERVAL`
type (and stored as `BIGINT` microseconds on other backends). Values are
exposed in Python as `datetime.timedelta`.

## Why?

PostgreSQL has a native `INTERVAL` column type for storing durations, but
Django ships no model field that maps to it. `IntervalField` fills that gap:
on PostgreSQL it uses the native `INTERVAL` type, and on other backends it
stores the duration as a `BIGINT` number of microseconds — so the same model
works everywhere while taking advantage of PostgreSQL where available.

## Features

- Native PostgreSQL `INTERVAL` column; `BIGINT` fallback for other backends
  (MySQL, SQLite, …)
- Maps to `datetime.timedelta`
- Configurable form widget with per-unit inputs (days/hours/minutes/seconds/
  microseconds) plus `min_value` / `max_value` validation
- Internationalized (ships Polish and German translations)
- Optional Dojango widget support
- Example/test Django project included

## Supported versions

Tested in CI against these Django × Python combinations:

| Django  | 3.10 | 3.11 | 3.12 | 3.13 | 3.14 |
|---------|------|------|------|------|------|
| 5.2 LTS | ✓    | ✓    | ✓    | ✓    | ✓    |
| 6.0     | —    | —    | ✓    | ✓    | ✓    |

## Installation

### Using uv (recommended)

```bash
uv add django-pgsql-interval-field
```

### Using pip

```bash
pip install django-pgsql-interval-field
```

Add `"interval"` to `INSTALLED_APPS` to pick up the widget's CSS and the
bundled translations.

## Quick start

```python
from datetime import timedelta

from django.db import models

from interval.fields import IntervalField


class Meeting(models.Model):
    # Stored as PostgreSQL INTERVAL, or BIGINT microseconds elsewhere.
    duration = IntervalField(default=timedelta(hours=1))

    # Restrict the form widget's units and range.
    break_time = IntervalField(
        format="HMS",
        min_value=timedelta(minutes=5),
        max_value=timedelta(hours=2),
        null=True,
        blank=True,
    )
```

Assign `datetime.timedelta` values (or a raw number of microseconds, or a
`"[D day[s], ]HH:MM:SS[.ffffff]"` string); reading the field always returns a
`timedelta`.

## License

MIT — see [LICENSE](LICENSE) for details.
