# Usage

## Installation

Clone the repository and install dependencies:

```bash
uv sync
```

## Running

Via the CLI entrypoint:

```bash
uv run second_brain                          # production defaults
uv run --env-file .env second_brain          # dev settings
```

Or as a Python module:

```bash
uv run python -m second_brain
```

## Log Format

Output uses a compact format with 3-character level abbreviations and consistent `|` separators:

```
2026-03-21 14:32:05 | INF | second_brain.app:main:29 | Hello from second_brain!
```

Level abbreviations: `DBG`, `INF`, `WRN`, `ERR`, `CRT`.

## Environment Variables

| Variable    | Default   | Description                        |
| ----------- | --------- | ---------------------------------- |
| `LOG_LEVEL` | `INFO`    | Console log level (DEBUG, INFO, …) |
| `LOG_FILE`  | `app.log` | Path to the log file               |

Copy `.env.example` to `.env` for development defaults, then run with `uv run --env-file .env`.
