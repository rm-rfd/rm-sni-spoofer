# AGENTS.md

## Purpose

This file is for repo-specific implementation guidance for coding agents. Read `README.md` first for product behavior, limits, requirements, configuration fields, run/build usage, and the high-level project layout. Keep changes small, local, and easy to validate. Favor root-cause fixes over broad refactors, especially in network and process-control code.

## Repo Facts

- CI builds on Python 3.11. Keep new code compatible with Python 3.11 even if local development is happening on a newer interpreter.
- There is currently no tracked unit-test suite or repo-level lint configuration. Do not invent nonexistent project commands in reviews or change notes.

## Do Not Edit

Only touch these when the task is explicitly about packaging, generated artifacts, or bundled binaries:

- `build/pyinstaller/`
- `build/spec/`
- `dist/`
- `.venv/`
- bundled runtime files under `xray/`

## Implementation Rules

1. Start from the module that directly decides the behavior, not the highest-level caller.
2. Make one small edit slice at a time, then validate before widening scope.
3. Keep `src/main.py` and `src/__main__.py` thin; new business logic belongs in the owning module.
4. Route config-backed behavior through `src/core/config/app_config.py`. Add new config fields there and in `config.json`.
5. Reuse existing path helpers such as `get_app_dir()`, `get_asset_path()`, and `resolve_runtime_path()`.
6. Treat `src/core/runtime/relay_server.py` and `src/core/packet_injection/` as timing-sensitive. Do not do style cleanups there without task-specific validation.
7. Preserve startup and cleanup symmetry. If you add a resource, add the matching stop, unlink, close, or unregister path in the same change.
8. Keep Windows-specific behavior isolated. Preserve current fallback behavior when touching `ctypes`, socket options, `taskkill`, or WinDivert assumptions.
9. Keep persistent state separate from widget state. Do not treat Tk widget contents as the source of truth.
10. Keep `src/gui/window.py` focused on orchestration. If a change grows beyond layout or shell behavior, move it into the nearest GUI helper.
11. Keep visual tokens in `src/gui/theme.py`.
12. Preserve the existing log-prefix convention. Known prefixes include `[start]`, `[stop]`, `[exit]`, `[delay]`, `[pid]`, `[profiles]`, `[loaded]`, `[support]`, and `[updates]`.

## Common Routing

For the broad project layout, use `README.md`. Use the routes below when deciding where implementation should live.

- CLI flags or bootstrap: `src/main.py`
- Config normalization or active profile persistence: `src/core/config/app_config.py`
- Runtime values, Xray startup, runtime path resolution: `src/core/runtime/runtime_state.py`
- Headless relay flow: `src/core/runtime/relay_server.py`
- Xray share-link logic: `src/core/xray/`
- GUI subprocess lifecycle: `src/services/relay_runtime.py`
- Delay testing: `src/services/delay_test.py`
- Profile-table behavior: `src/gui/profiles.py`
- Relay start/stop UI actions: `src/gui/relay.py`
- GUI log formatting/routing: `src/gui/logs.py`
- Theme, icons, log tag mapping: `src/gui/theme.py`

## Update Together

- New or renamed config field: `config.json`, `src/core/config/app_config.py`, and every runtime or GUI consumer; update `README.md` if user-facing.
- Runtime startup, packaged assets, or bundled files: `build.py` and `README.md`; if release layout changes, also update `.github/workflows/build-release.yml`.
- New runtime dependency: `requirements.txt`. Packaging-only dependency: `requirements-build.txt`.
- New log prefix: update `src/gui/theme.py` and any dependent GUI log code in the same change.
- Large new feature: add notes under `implementation-docs/`.

## Validation

- Always run the narrowest relevant validation after a change.
- Safe verified checks in this repo:
  - `py -m compileall src build.py`
  - `python -m src --help`
  - `python build.py --dry-run`
- Use validation by surface area:
  - `src/core/config/` only: `py -m compileall src build.py`; add `python -m src --help` if CLI wiring changed.
  - `src/core/xray/`, `src/core/runtime/`, `src/services/`: `py -m compileall src build.py`; add the narrowest runnable smoke check that does not require privileged packet injection.
  - `src/gui/` only: `py -m compileall src build.py`; add `python -m src --help` if startup or imports changed.
  - `build.py` or release layout: `python build.py --dry-run`.
- Full runtime checks may require administrator privileges, WinDivert via `pydivert`, reachable network routes, and `xray\\xray.exe`. If you cannot run them, say so clearly and still run the cheapest available smoke check.

## Definition Of Done

- The change stays in the owning module instead of scattering new control paths across the repo.
- Config, runtime, GUI, packaging, startup, shutdown, persistence, and logging remain internally consistent for the touched feature.
- User-visible behavior changes are documented in `README.md` when needed.
- The narrowest applicable validation was run and reported.
- Generated files and bundled artifacts were not edited unless the task required it.
