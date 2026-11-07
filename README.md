# Janus Core

[![CI](https://github.com/RohanHarish6/janus-core-open-source/actions/workflows/ci.yml/badge.svg)](https://github.com/RohanHarish6/janus-core-open-source/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Contributors](https://img.shields.io/github/contributors/RohanHarish6/janus-core-open-source)](https://github.com/RohanHarish6/janus-core-open-source/graphs/contributors)

> An open-source Windows-oriented multi-agent AI workbench with local-first
> routing, security checks, and an animated cityscape interface.

Janus Core is an experimental desktop suite for coordinating local and
optional remote language-model tiers. It includes a command/search workbench,
agent routing, a security auditor, creative tooling, OpenAPI documentation,
and Windows launch/build scripts.

This repository is intentionally transparent about its status. Some routing
providers and model names are integrations or experiments rather than bundled
services. Janus Core does not include model weights, API credentials, private
telemetry, generated reports, or installer binaries.

## What is included

| Area | Key files |
| --- | --- |
| Desktop server and API | `desktop_app.py`, `openapi.json` |
| Routing and orchestration | `token_optimized_multiagent.py`, `model_router.py`, `janus_core_engine_v3_7_0.py` |
| Security controls | `security_manager.py`, `preflight_audit.py`, `test_security_auditor.py` |
| Creative workspace | `creative_studio.py`, `creative_studio_live.py` |
| Interface | `cityscape_agent_dashboard.html`, `results_window.html` |
| Windows packaging | `Run_Janus_Core.bat`, `Install_Janus_Core_Full_System.ps1`, `build_installer.bat` |
| Agent workflows | `.agents/` |
| Tests and specifications | `tests/`, `specs/` |

## Quick start

Janus Core targets Python 3.10–3.12 on Windows.

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
Copy-Item .env.example .env
python desktop_app.py
```

Open `http://127.0.0.1:8765`. For the original one-click workflow, run
`Run_Janus_Core.bat` after installing the required local services.

## Configuration and privacy

Copy `.env.example` to `.env` and set only the providers you intend to use.
Never commit `.env`, API keys, model weights, telemetry, or personal datasets.
The default template binds services to localhost. Review provider and internet
research settings before enabling them.

## Testing

```powershell
python run_tests.py
python -m unittest discover tests
```

The source snapshot currently has known test-runner failures that need
community triage. The project is published with those tests and their
fixtures so contributors can reproduce and improve the baseline rather than
receiving a falsely “green” status.

## Contributing

Janus Core is open source and welcomes contributions. Useful areas include:

- making routing providers configurable and testable;
- improving local-only operation and hardware guardrails;
- strengthening prompt-injection, PII, and output handling defenses;
- fixing the current test baseline and adding regression coverage;
- improving accessibility and responsiveness of the cityscape UI;
- documenting setup for Linux and macOS;
- replacing speculative integrations with reliable adapters.

Read [CONTRIBUTING.md](CONTRIBUTING.md), choose an issue, or open a discussion
before starting a large architectural change. If this project interests you,
star it and share it with local-AI, privacy, security, and agent-tooling
communities so more contributors can help shape it.

## License

Janus Core is released under the [MIT License](LICENSE).
