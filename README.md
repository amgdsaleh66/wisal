# Wisal (وصال)

**A bilingual (Arabic/English) CLI tool to convert data between JSON, CSV, and YAML.**

## Why Wisal?

Most data conversion tools (jc, Miller, dasel...) are excellent but entirely English: error messages, warnings, even documentation. This creates a real barrier for thousands of Arabic-speaking developers, especially when debugging complex data.

Wisal is a small, focused tool that solves exactly this problem:

- 🌐 Every message (error, warning, help) is available in Arabic and English, auto-detected from the system locale (defaults to English)
- 🔢 Detects and handles Arabic-Indic digits (٠-٩) mixed with Latin digits in the same data
- 🔤 Detects common encoding issues (Windows-1256 vs UTF-8) that corrupt Arabic text
- ✅ Validates data quality before converting (mixed types, nested fields) instead of silently failing
- 📦 No bloat: one tool, one command, predictable behavior

## Installation

```bash
pip install wisal-cli
```

Or from source:

```bash
git clone https://github.com/amgdsaleh66/wisal.git
cd wisal
pip install -e .
```

## Usage

```bash
# Simple conversion
wisal convert data.json data.csv

# Force Arabic messages
wisal convert data.json data.csv --lang ar

# Flatten nested fields when converting to CSV
wisal convert data.json data.csv --flatten

# Normalize Arabic-Indic digits to Latin
wisal convert data.json data.csv --normalize-digits

# Preview output without saving
wisal convert data.json data.csv --dry-run
```

Run `wisal --help` or `wisal convert --help` for the full list of options.

### Example

**input.json:**
```json
[
  {"name": "Ahmad", "age": "٣٠", "city": "Riyadh"},
  {"name": "Sara", "age": 25, "city": "Dubai"}
]
```

```bash
wisal convert input.json output.csv --normalize-digits
```

```
⚠ Warning: Column 'age' has mixed data types (e.g. numbers and text together) in rows: 1, 2.
Successfully converted 'input.json' to 'output.csv'. (2 rows/items)
```

## Supported Formats

| From \ To | JSON | CSV | YAML |
|-----------|------|-----|------|
| JSON      | —    | ✅  | ✅   |
| CSV       | ✅   | —   | ✅   |
| YAML      | ✅   | ✅  | —    |

## Contributing

Contributions welcome! Open an issue or pull request.

```bash
pip install -e ".[dev]"
pytest tests/
```

See [CONTRIBUTING.md](CONTRIBUTING.md) for details.

## License

MIT
