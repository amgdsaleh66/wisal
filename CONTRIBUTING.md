# Contributing to Wisal

Thanks for your interest in contributing!

## Getting Started

```bash
git clone https://github.com/amgdsaleh66/wisal.git
cd wisal
pip install -e ".[dev]"
pytest tests/
```

## Adding New Messages

All user-facing messages live in `wisal/messages.py`. When adding a new
message, you must provide both Arabic and English versions at the same time,
since bilingual support is the core feature of this project.

## Submitting a Pull Request

1. Fork the project
2. Create a new branch (`git checkout -b feature/my-feature`)
3. Make sure the tests pass (`pytest tests/`)
4. Open a Pull Request with a clear description of the change
