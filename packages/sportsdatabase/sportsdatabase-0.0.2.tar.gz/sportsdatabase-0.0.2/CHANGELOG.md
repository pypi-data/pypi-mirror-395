# Changelog

All notable changes to the Python SDK will be documented in this file.

## Unreleased

- Hardened HTTP client parsing with stricter typing and rate-limit metadata guarantees.
- Added pytest coverage for every endpoint plus HTTP retry behavior; Hatch `lint`/`typecheck`/`test` now gate releases.
- README updated with endpoint table, dev commands, and release flow pointer (`docs/release-checklist.md`).

## 0.0.1 - 2025-12-05

- Initial release candidate mirroring the TypeScript SDK design.
- Implements clients/endpoints for leagues, teams, events, schedules, and scores.
- Provides httpx-based HTTP client with retries, rate-limit metadata, and typed errors.
- Includes example scripts, pytest suites, linting (Ruff), and type checking (Mypy) via Hatch.
