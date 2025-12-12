# deprecat

Developer tooling that scans Python codebases for third-party API (TPA) usage, and returns verified patch suggestions. Built for the [Gemini 3 Hackathon](https://cerebralvalley.ai/e/gemini-3-hack-sf/details).

## Quickstart 
1. `uv venv && source .venv/bin/activate`
2. `uv sync --dev`
3. `cp docs/config/.env.sample .env` and insert your Google AI Studio credentials.
4. `deprecat doctor`
5. `deprecat init` — guided setup to choose monitored packages and scan cadence
6. `deprecat packages` — inspect dependencies detected from `pyproject.toml` and highlight the monitored subset
7. `deprecat scan . --packages sentry-sdk,slack_sdk` — produce a timestamped index under `.deprecat/indexes/` for the packages you care about
8. `deprecat show -t` — list available scan timestamps
9. `deprecat analyze --endpoint http://127.0.0.1:8080` — send the latest scan to the backend mock and view suggestions
10. `deprecat serve --reload` — run the local FastAPI backend (for development/testing)

## CLI
- `deprecat doctor` — verifies Python version, detects `.env`, checks Google AI Studio credentials, and ensures `.deprecat/logs` plus `.deprecat/checkpoints` are writable. Outputs a summary table and stores the run in `.deprecat/logs/doctor.log`.
- `deprecat init` — interactive setup for choosing monitored TPAs and scan frequency; writes `.deprecat/config.json`.
- `deprecat config [path]` — display the stored configuration or tweak via `--packages/--frequency`.
- `deprecat packages [path]` — list dependencies discovered from `pyproject.toml`/`requirements` and flag which ones are monitored.
- `deprecat analyze [path]` — send the selected snapshot to the backend (`--endpoint` override) and render returned suggestions.
- `deprecat scan [path]` — walks a Python repo, collects import usage, and writes a timestamped index JSON under `.deprecat/indexes/`. Use `--packages pkg1,pkg2` (or set them in `.deprecat/config.json`) to limit scans to the TPAs you monitor.
- `deprecat show [path]` — displays the most recent index snapshot (`--timestamp <ts>` for specific snapshots, `-t/--timestamps` to list all timestamps, `--limit N`/`--all` to control output size).
- `deprecat serve` — start the mocked FastAPI backend (defaults to `http://127.0.0.1:8080`) so the CLI can call `/analyze`.

Future commands (`review`, `schedule`) will follow the same `deprecat <command>` pattern once implemented.

## Configuration
- `deprecat init` is the quickest way to bootstrap `.deprecat/config.json`.
- Prefer editing the config via `deprecat config --packages pkg1,pkg2 --frequency 7` when scripting.
- A sample skeleton lives in `docs/config/config.sample.json`.
- Runtime artifacts (logs, checkpoints, temporary folders) remain under `.deprecat/` so deleting that directory resets state.

## Backend Service
- The mocked FastAPI backend lives at `src/deprecat/backends/server.py` with `/health` and `/analyze` endpoints.
- Run `deprecat serve-backend --reload` while developing to expose the API locally. The CLI will target `http://127.0.0.1:8000` by default until the real remote service is wired up.

## Project Layout
```
src/deprecat/       # CLI, scanner, backend clients, scheduler
assets/samples/     # Mock manifests + payloads
.deprecat/          # Logs and checkpoints (git-ignored)
tests/              # Pytest suites mirroring source layout
docs/               # Architecture notes, UI flows, config samples
```

## Contributing
- Follow the workflow in `AGENTS.md` for coding standards, testing, and checkpoint hand-offs.
- Every feature addition must create a checkpoint under `.deprecat/checkpoints/<timestamp>-<feature>/` with diffs, verification output, and TODOs for the next agent.
