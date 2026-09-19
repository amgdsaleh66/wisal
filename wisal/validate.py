"""
Data quality checks prior to conversion: mixed types, mixed digits, missing fields.
"""

from typing import Any

from wisal.arabic_utils import detect_column_digit_issues
from wisal.messages import t


def _python_type_name(value: Any) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "bool"
    if isinstance(value, (int, float)):
        return "number"
    return "text"


def validate_rows(rows: list[dict], warn) -> None:
    """
    Run all quality checks on a list of rows (already normalized to dicts)
    and emit warnings through the provided warn function.
    """
    if not rows:
        return

    columns: dict[str, list] = {}
    for row in rows:
        if not isinstance(row, dict):
            continue
        for key, value in row.items():
            columns.setdefault(key, []).append(value)

    for column, values in columns.items():
        # Check for mixed types
        types_seen = {}
        for idx, value in enumerate(values):
            type_name = _python_type_name(value)
            if type_name in ("null",):
                continue
            types_seen.setdefault(type_name, []).append(idx + 1)

        non_null_types = [k for k in types_seen if k != "null"]
        if len(non_null_types) > 1:
            all_lines = sorted({ln for lns in types_seen.values() for ln in lns})
            warn(
                t(
                    "validation_type_mismatch",
                    column=column,
                    lines=", ".join(str(x) for x in all_lines[:10]),
                )
            )

        # Check for mixed Arabic-Indic/Latin digits
        str_values = [v for v in values if isinstance(v, str)]
        if str_values and detect_column_digit_issues(str_values):
            warn(t("mixed_digits_warning", column=column))
