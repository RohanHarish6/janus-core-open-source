# Contributing to Janus Core

Thank you for helping make Janus Core safer, more local-first, and more
reliable.

## Development setup

Janus Core currently targets Windows and Python 3.10–3.12:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

Run the test suite before opening a pull request:

```powershell
python run_tests.py
python -m unittest discover tests
```

## Contribution guidelines

- Keep changes focused and explain the user-visible outcome.
- Preserve localhost-first defaults and explicit provider permissions.
- Do not commit credentials, `.env`, model weights, telemetry, private
  datasets, generated installers, or personal data.
- Add regression tests for routing, security, configuration, or API changes.
- Keep claims about model capability measurable and reproducible.
- Update documentation when setup or behavior changes.

## Pull requests

Include what changed, why it matters, how you tested it, compatibility notes,
and known limitations. UI changes should include a screenshot or short
recording. Open an issue or discussion before large architectural changes.
