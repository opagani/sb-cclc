# How This Project Was Built

A step-by-step walkthrough of scaffolding the `second-brain` Python project from scratch using Claude Code.

---

## Step 1: Run the scaffold prompt

The scaffold prompt lives in `scaffold-second-brain-python.md`. To use it, open Claude Code in your target directory and paste (or `@`-reference) that file.

Claude will ask you three questions:

| Question | Answer used here |
|---|---|
| Project/package name | `second_brain` |
| Starting version | `0.0.1` |
| Where to scaffold | Current directory |

---

## Step 2: Claude creates the project structure

Claude generates the following layout:

```
sb/
├── src/
│   └── second_brain/
│       ├── __init__.py       # empty, marks it as a package
│       ├── __main__.py       # allows `python -m second_brain`
│       └── app.py            # main logic lives here
├── tests/
│   ├── __init__.py
│   ├── conftest.py           # shared fixtures (redirects log file in tests)
│   └── test_app.py           # starter test
├── scripts/
│   └── serve_docs.py         # runs mkdocs serve + tees output to mkdocs.log
├── docs/
│   ├── index.md
│   ├── usage.md
│   └── api.md
├── mkdocs.yml                # Material for MkDocs config
├── pyproject.toml            # single source of truth for all config
├── README.md
├── .gitignore                # based on github/gitignore Python template
├── .env.example              # committed — template for developers
├── .env                      # NOT committed — dev environment
└── .env.test                 # NOT committed — loaded automatically by pytest
```

---

## Step 3: Understand the key files

### `pyproject.toml`

Everything lives here — no `setup.py`, no `setup.cfg`.

- **Build backend:** `uv_build`
- **Package name:** `second-brain` (hyphenated, for PyPI)
- **Import name:** `second_brain` (underscored, for Python)
- **Entrypoint:** `second_brain` CLI command → calls `second_brain.app:main`
- **Linter/formatter:** `ruff` (replaces flake8 + black + isort)
- **Test runner:** `pytest` with `pytest-cov` and `pytest-env`
- **Docs:** MkDocs + Material theme + mkdocstrings

### `src/second_brain/app.py`

Two functions:

1. **`configure_logging()`** — sets up loguru with two handlers:
   - stderr at `LOG_LEVEL` (default `INFO`) — what you see in the terminal
   - file at `DEBUG` level writing to `LOG_FILE` (default `app.log`) — full detail on disk

2. **`main()`** — decorated with `@logger.catch` so unhandled exceptions are logged with a full traceback instead of a raw Python crash. Calls `configure_logging()` then logs a greeting.

### `tests/conftest.py`

Contains an `autouse` fixture that redirects `LOG_FILE` to pytest's `tmp_path` for every test. This prevents tests from writing to `app.log` in the project root.

### Environment files

| File | Committed? | Purpose |
|---|---|---|
| `.env.example` | Yes | Template — copy to `.env` |
| `.env` | No | Dev overrides — loaded with `--env-file .env` |
| `.env.test` | No | Test overrides — auto-loaded by `pytest-env` |

---

## Step 4: Install dependencies

```bash
uv sync
```

This creates `.venv/` and installs all dependencies (including dev group). Also builds and installs the local `second-brain` package in editable mode.

---

## Step 5: Verify everything works

```bash
uv run pytest
```

Expected output:

```
1 passed in 0.12s
```

The test calls `main()`, captures stderr, and asserts the greeting appears.

---

## Step 6: Run the app

```bash
# Production defaults (LOG_LEVEL=INFO)
uv run second_brain

# With dev environment (LOG_LEVEL=DEBUG)
uv run --env-file .env second_brain

# As a module
uv run python -m second_brain
```

Both runs write to `app.log` as well as the terminal.

---

## Step 7: Run tests with coverage

```bash
uv run pytest --cov
```

Coverage is configured to:
- Track branch coverage
- Source from `src/`
- Fail if coverage drops below 80%
- Exclude `__main__.py`

---

## Step 8: Preview the documentation

```bash
uv run python scripts/serve_docs.py
```

Opens MkDocs dev server at `http://127.0.0.1:8000`. Output is also written to `mkdocs.log` so Claude Code can read it.

To build static HTML:

```bash
uv run mkdocs build
```

Output goes to `site/` (which is gitignored).

---

## Step 9: Commit to version control

```bash
git init
git add .
git commit -m "Initial scaffold"
```

Key things to commit:
- `uv.lock` — ensures reproducible installs for everyone
- `.env.example` — documents required environment variables

Key things **not** to commit (already in `.gitignore`):
- `.env`, `.env.test` — contain local/secret values
- `.venv/`, `app.log`, `site/`, `htmlcov/`

---

## Extending the project

From here, the typical workflow is:

1. Add your logic to `src/second_brain/app.py` (or add new modules alongside it)
2. Write tests in `tests/`
3. Run `uv run pytest --cov` to check coverage
4. Run `uv run ruff check . && uv run ruff format .` to lint and format
5. Update `docs/` as features grow
