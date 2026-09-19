"""
Command-line interface for the Wisal tool.

Usage:
    wisal convert input.json output.csv
    wisal convert data.csv data.yaml --flatten
    wisal convert data.json out.csv --dry-run --lang ar
"""

import argparse
import os
import sys
from pathlib import Path

from wisal.arabic_utils import normalize_digits
from wisal.errors import WisalError
from wisal.formats import format_from_extension, load_data, write_data, write_stdout
from wisal.messages import Lang, detect_language, t
from wisal.validate import validate_rows

__version__ = "0.1.0"


def _apply_digit_normalization(data):
    """Recursively apply digit normalization to every string in the structure."""
    if isinstance(data, dict):
        return {k: _apply_digit_normalization(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_apply_digit_normalization(v) for v in data]
    if isinstance(data, str):
        return normalize_digits(data)
    return data


def build_parser() -> argparse.ArgumentParser:
    lang_parent = argparse.ArgumentParser(add_help=False)
    lang_parent.add_argument(
        "--lang",
        choices=["ar", "en"],
        default=None,
        help="Message language (ar/en). Default: auto-detect from system locale.",
    )

    parser = argparse.ArgumentParser(
        prog="wisal",
        description=(
            "Wisal — a bilingual (Arabic/English) data conversion tool for JSON, CSV, and YAML."
        ),
        formatter_class=argparse.RawDescriptionHelpFormatter,
        parents=[lang_parent],
    )
    parser.add_argument(
        "--version", action="version", version=f"wisal {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    convert = subparsers.add_parser(
        "convert",
        help="Convert a file from one format to another",
        parents=[lang_parent],
    )
    convert.add_argument("input", help="Input file")
    convert.add_argument("output", help="Output file")
    convert.add_argument(
        "--flatten",
        action="store_true",
        help="Flatten nested fields into columns (for CSV output)",
    )
    convert.add_argument(
        "--normalize-digits",
        action="store_true",
        help="Normalize Arabic-Indic digits (٠-٩) to Latin digits",
    )
    convert.add_argument(
        "--dry-run",
        action="store_true",
        help="Preview output without writing a file",
    )
    convert.add_argument(
        "--no-validate",
        action="store_true",
        help="Skip data quality checks",
    )
    convert.add_argument(
        "--quiet",
        action="store_true",
        help="Suppress warnings, show only errors",
    )

    return parser


def run(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.lang:
        os.environ["WISAL_LANG"] = args.lang
    lang = Lang(args.lang) if args.lang else detect_language()

    def warn(message: str) -> None:
        if not getattr(args, "quiet", False):
            print(f"⚠ {message}", file=sys.stderr)

    if args.command == "convert":
        input_path = Path(args.input)
        output_path = Path(args.output)

        try:
            data = load_data(input_path, warn=warn)

            if args.normalize_digits:
                data = _apply_digit_normalization(data)

            if not args.no_validate:
                rows = data if isinstance(data, list) else [data]
                validate_rows(rows, warn=warn)

            if args.dry_run:
                out_fmt = format_from_extension(output_path)
                write_stdout(data, out_fmt, flatten=args.flatten, warn=warn)
                print(t("dry_run_notice", lang=lang), file=sys.stderr)
            else:
                write_data(data, output_path, flatten=args.flatten, warn=warn)
                row_count = len(data) if isinstance(data, list) else 1
                print(
                    t(
                        "conversion_success",
                        lang=lang,
                        source=str(input_path),
                        target=str(output_path),
                        rows=row_count,
                    )
                )
        except WisalError as e:
            print(f"✗ {e}", file=sys.stderr)
            return 1

    return 0


def main() -> None:
    sys.exit(run())


if __name__ == "__main__":
    main()
