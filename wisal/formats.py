"""
Reading and writing supported data formats: JSON, CSV, YAML.
"""

import csv
import json
import sys
from pathlib import Path
from typing import Any

import yaml

from wisal.arabic_utils import likely_encoding_issue
from wisal.errors import WisalError
from wisal.messages import t

SUPPORTED_FORMATS = ("json", "csv", "yaml", "yml")


def format_from_extension(path: Path) -> str:
    ext = path.suffix.lstrip(".").lower()
    if ext == "yml":
        ext = "yaml"
    if ext not in SUPPORTED_FORMATS:
        raise WisalError(t("unsupported_format", ext=ext or "(none)"))
    return ext


def read_file_bytes(path: Path) -> bytes:
    if not path.exists():
        raise WisalError(t("file_not_found", path=str(path)))
    raw = path.read_bytes()
    if len(raw) == 0:
        raise WisalError(t("empty_input", path=str(path)))
    return raw


def load_data(path: Path, warn) -> Any:
    """
    Load data from a file based on its extension, checking encoding along the way.
    """
    fmt = format_from_extension(path)
    raw = read_file_bytes(path)

    detected_encoding = likely_encoding_issue(raw)
    if detected_encoding:
        warn(t("encoding_mismatch_warning", detected=detected_encoding))
        text = raw.decode(detected_encoding, errors="replace")
    else:
        text = raw.decode("utf-8")

    if fmt == "json":
        try:
            return json.loads(text)
        except json.JSONDecodeError as e:
            raise WisalError(
                t("invalid_json", line=e.lineno, column=e.colno, detail=e.msg)
            ) from e

    if fmt == "yaml":
        try:
            return yaml.safe_load(text)
        except yaml.YAMLError as e:
            raise WisalError(str(e)) from e

    if fmt == "csv":
        reader = csv.DictReader(text.splitlines())
        return list(reader)

    raise WisalError(t("unsupported_format", ext=fmt))


def _flatten_dict(d: dict, parent_key: str = "", sep: str = ".") -> dict:
    items = {}
    for k, v in d.items():
        new_key = f"{parent_key}{sep}{k}" if parent_key else str(k)
        if isinstance(v, dict):
            items.update(_flatten_dict(v, new_key, sep=sep))
        else:
            items[new_key] = v
    return items


def _rows_from_data(data: Any, flatten: bool, warn) -> list[dict]:
    """Normalize any data structure (list or object) into a list of CSV-ready rows."""
    if isinstance(data, dict):
        data = [data]
    if not isinstance(data, list):
        raise WisalError(t("unsupported_format", ext="(structure)"))

    rows = []
    for row in data:
        if not isinstance(row, dict):
            rows.append({"value": row})
            continue
        new_row = {}
        for key, value in row.items():
            if isinstance(value, (dict, list)):
                if flatten and isinstance(value, dict):
                    new_row.update(_flatten_dict({key: value}))
                else:
                    warn(t("nested_structure_warning", field=key))
                    new_row[key] = json.dumps(value, ensure_ascii=False)
            else:
                new_row[key] = value
        rows.append(new_row)
    return rows


def write_data(data: Any, path: Path, flatten: bool, warn) -> None:
    """
    Write data to a file based on its extension.
    """
    fmt = format_from_extension(path)

    if fmt == "json":
        path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")
        return

    if fmt == "yaml":
        path.write_text(
            yaml.dump(data, allow_unicode=True, sort_keys=False), encoding="utf-8"
        )
        return

    if fmt == "csv":
        rows = _rows_from_data(data, flatten=flatten, warn=warn)
        if not rows:
            path.write_text("", encoding="utf-8")
            return
        fieldnames = list(dict.fromkeys(k for row in rows for k in row.keys()))
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for row in rows:
                writer.writerow(row)
        return

    raise WisalError(t("unsupported_format", ext=fmt))


def write_stdout(data: Any, fmt: str, flatten: bool, warn) -> None:
    """Write the output to stdout (for dry-run preview mode)."""
    if fmt == "json":
        sys.stdout.write(json.dumps(data, ensure_ascii=False, indent=2) + "\n")
    elif fmt == "yaml":
        sys.stdout.write(yaml.dump(data, allow_unicode=True, sort_keys=False))
    elif fmt == "csv":
        rows = _rows_from_data(data, flatten=flatten, warn=warn)
        if not rows:
            return
        fieldnames = list(dict.fromkeys(k for row in rows for k in row.keys()))
        writer = csv.DictWriter(sys.stdout, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
