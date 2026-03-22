import re

from loguru import logger

from second_brain.app import FORMAT, configure_logging


def test_format_constant_contains_expected_parts():
    assert "{time:YYYY-MM-DD HH:mm:ss}" in FORMAT
    assert "{level.name:.3}" in FORMAT
    assert "{message}" in FORMAT


def test_timestamp_has_no_milliseconds(capfd):
    configure_logging()
    logger.info("test")
    captured = capfd.readouterr()
    # Match YYYY-MM-DD HH:MM:SS but ensure no trailing .digits (milliseconds)
    assert re.search(r"\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \|", captured.err)


def test_level_is_three_char_abbreviation(capfd):
    configure_logging()
    logger.info("test")
    captured = capfd.readouterr()
    assert "| INF |" in captured.err
    assert "INFO" not in captured.err


def test_consistent_separator(capfd):
    configure_logging()
    logger.info("test")
    captured = capfd.readouterr()
    # The old format used " - " before the message; new format uses " | " throughout
    assert " - " not in captured.err
