import json
import subprocess
import sys
from pathlib import Path

import pytest

from wisal.arabic_utils import (
    contains_arabic_indic_digits,
    has_mixed_digits,
    normalize_digits,
)
from wisal.messages import Lang, t


def test_normalize_digits():
    assert normalize_digits("٢٥") == "25"
    assert normalize_digits("age ٣٠ years") == "age 30 years"
    assert normalize_digits("no digits here") == "no digits here"


def test_contains_arabic_indic_digits():
    assert contains_arabic_indic_digits("٥") is True
    assert contains_arabic_indic_digits("5") is False


def test_has_mixed_digits():
    assert has_mixed_digits("٢5") is True
    assert has_mixed_digits("25") is False
    assert has_mixed_digits("٢٥") is False


def test_messages_arabic():
    msg = t("file_not_found", lang=Lang.AR, path="test.json")
    assert "test.json" in msg
    assert "غير موجود" in msg


def test_messages_english():
    msg = t("file_not_found", lang=Lang.EN, path="test.json")
    assert "test.json" in msg
    assert "not found" in msg


def test_convert_json_to_csv(tmp_path):
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.csv"
    input_file.write_text(
        json.dumps([{"name": "Ali", "age": 20}, {"name": "Sara", "age": 22}]),
        encoding="utf-8",
    )

    result = subprocess.run(
        [sys.executable, "-m", "wisal.cli", "convert", str(input_file), str(output_file), "--lang", "en"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert output_file.exists()
    content = output_file.read_text(encoding="utf-8")
    assert "name,age" in content
    assert "Ali,20" in content


def test_convert_missing_file_returns_error(tmp_path):
    result = subprocess.run(
        [sys.executable, "-m", "wisal.cli", "convert", str(tmp_path / "nope.json"), str(tmp_path / "out.csv")],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "✗" in result.stderr


def test_convert_json_to_yaml(tmp_path):
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.yaml"
    input_file.write_text(json.dumps({"key": "قيمة"}), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "wisal.cli", "convert", str(input_file), str(output_file), "--lang", "en"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    content = output_file.read_text(encoding="utf-8")
    assert "قيمة" in content


def test_convert_directory_input_returns_clean_error(tmp_path):
    input_dir = tmp_path / "input.json"
    input_dir.mkdir()
    result = subprocess.run(
        [sys.executable, "-m", "wisal.cli", "convert", str(input_dir), str(tmp_path / "out.csv"), "--lang", "en"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 1
    assert "Traceback" not in result.stderr
    assert "was not found" in result.stderr


def test_dry_run_does_not_write_file(tmp_path):
    input_file = tmp_path / "input.json"
    output_file = tmp_path / "output.csv"
    input_file.write_text(json.dumps([{"a": 1}]), encoding="utf-8")

    result = subprocess.run(
        [sys.executable, "-m", "wisal.cli", "convert", str(input_file), str(output_file), "--dry-run", "--lang", "en"],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert not output_file.exists()
