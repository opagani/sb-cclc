# second-brain

## Installation

Clone the repository and install dependencies:

```bash
git clone <repo-url>
cd second-brain
uv sync
```

## Usage

Via the CLI entrypoint:

```bash
uv run second_brain
```

With dev environment:

```bash
uv run --env-file .env second_brain
```

Via Python module:

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

Copy `.env.example` to `.env` for development defaults:

```bash
cp .env.example .env
```

Then load it explicitly when running: `uv run --env-file .env second_brain` (no auto-loading).

| Variable    | Default   | Description                                          |
| ----------- | --------- | ---------------------------------------------------- |
| `LOG_LEVEL` | `INFO`    | Console log level. Set to `DEBUG` in `.env` for verbose output. |
| `LOG_FILE`  | `app.log` | Path to the log file.                                |

## Testing

Run tests:

```bash
uv run pytest
```

Run tests with coverage:

```bash
uv run pytest --cov
```

## Documentation

Preview docs locally:

```bash
uv run python scripts/serve_docs.py
```

Build static docs:

```bash
uv run mkdocs build
```
