"""Tests for the CLI commands (new, list)."""

import pathlib
import re

import pytest
from click.testing import CliRunner

from second_brain.app import cli


@pytest.fixture
def runner():
    return CliRunner()


@pytest.fixture
def notes_dir(tmp_path, monkeypatch):
    d = tmp_path / "notes"
    monkeypatch.setenv("NOTES_DIR", str(d))
    return d


# -- second_brain new --


def test_new_creates_markdown_file(runner, notes_dir):
    result = runner.invoke(cli, ["new", "My brilliant idea"])
    assert result.exit_code == 0
    files = list(notes_dir.glob("*.md"))
    assert len(files) == 1


def test_new_file_contains_thought_text(runner, notes_dir):
    runner.invoke(cli, ["new", "My brilliant idea"])
    files = list(notes_dir.glob("*.md"))
    content = files[0].read_text()
    assert "My brilliant idea" in content


def test_new_filename_is_timestamp(runner, notes_dir):
    runner.invoke(cli, ["new", "Test thought"])
    files = list(notes_dir.glob("*.md"))
    # Expect YYYY-MM-DD_HHMMSS.md
    assert re.match(r"\d{4}-\d{2}-\d{2}_\d{6}\.md", files[0].name)


def test_new_creates_directory_if_missing(runner, notes_dir):
    assert not notes_dir.exists()
    result = runner.invoke(cli, ["new", "First thought"])
    assert result.exit_code == 0
    assert notes_dir.exists()


def test_new_confirms_save(runner, notes_dir):
    result = runner.invoke(cli, ["new", "Some thought"])
    assert "Saved" in result.output


# -- second_brain list --


def test_list_shows_storage_path(runner, notes_dir):
    notes_dir.mkdir(parents=True)
    result = runner.invoke(cli, ["list"])
    assert str(notes_dir) in result.output


def test_list_shows_numbered_filenames(runner, notes_dir):
    notes_dir.mkdir(parents=True)
    (notes_dir / "2026-03-21_140000.md").write_text("First")
    (notes_dir / "2026-03-21_150000.md").write_text("Second")
    result = runner.invoke(cli, ["list"])
    assert "1. 2026-03-21_140000.md" in result.output
    assert "2. 2026-03-21_150000.md" in result.output


def test_list_empty_directory(runner, notes_dir):
    notes_dir.mkdir(parents=True)
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "No notes" in result.output


def test_list_missing_directory(runner, notes_dir):
    assert not notes_dir.exists()
    result = runner.invoke(cli, ["list"])
    assert result.exit_code == 0
    assert "No notes" in result.output


# -- NOTES_DIR default --


def test_default_notes_dir_is_home(runner, monkeypatch):
    monkeypatch.delenv("NOTES_DIR", raising=False)
    result = runner.invoke(cli, ["list"])
    assert str(pathlib.Path.home() / "second_brain") in result.output
