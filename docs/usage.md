# Usage

## Installation

Clone the repository and install dependencies:

```bash
uv sync
```

## Commands

### Save a new thought

```bash
uv run second_brain new "My brilliant idea about caching"
```

This creates a timestamped markdown file (e.g., `2026-03-21_143205.md`) in your notes directory.

### List saved notes

```bash
uv run second_brain list
```

Example output:

```
Notes in: /Users/you/second_brain
1. 2026-03-21_143205.md
2. 2026-03-21_160012.md
```

### Running with dev settings

```bash
uv run --env-file .env second_brain new "Another thought"
```

Or as a Python module:

```bash
uv run python -m second_brain new "Works this way too"
```

## Log Format

Output uses a compact format with 3-character level abbreviations and consistent `|` separators:

```
2026-03-21 14:32:05 | INF | second_brain.app:new:55 | Saved note: 2026-03-21_143205.md
```

Level abbreviations: `DBG`, `INF`, `WRN`, `ERR`, `CRT`.

## Environment Variables

| Variable    | Default            | Description                          |
|-------------|--------------------|--------------------------------------|
| `NOTES_DIR` | `~/second_brain`   | Directory where notes are stored     |
| `LOG_LEVEL` | `INFO`             | Console log level (DEBUG, INFO, …)   |
| `LOG_FILE`  | `app.log`          | Path to the log file                 |

Copy `.env.example` to `.env` for development defaults, then run with `uv run --env-file .env`.
