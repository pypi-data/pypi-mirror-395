# promptkitx

Prompt pack manager that drops AGENTS snippets and `.agent` templates into a repo. Ships with the ExecPlan pack and is ready to host more packs later. PyPI: `promptkitx` · npm: `promptkitx`.

## Quick use (no install)

- Python/uvx (PyPI): `uvx promptkitx install execplan`
- Python/uvx (from GitHub tip): `uvx --from git+https://github.com/mikewong23571/promptkit.git promptkit install execplan`
- Node/npx: `npx promptkitx install execplan`

Both commands are idempotent and cache their envs. Add `-p /path/to/repo` to target another repo and `--force` to overwrite existing files.

## Install (optional)

- Python: `pip install promptkitx` or `pipx install promptkitx`
- Node: `npm install -g promptkitx` (or use `npx` per above)

## Commands (Python & Node CLIs)

- `promptkit list [-p PATH]` — show available built-in packs and installed packs in PATH (default `.`)
- `promptkit install <pack> [-p PATH] [--force]` — install/update a pack (built-in: `execplan`)

## Pack spec (v1)

Each pack lives under `src/promptkit_builtin_packs/<name>/` and contains:

- `pack.json` — metadata
  - `name`, `version`, `description`
  - `agents_entry`: relative path to the snippet inserted into `AGENTS.md`
  - `files`: array of `{ "source": "files/PLANS.md", "target": ".agent/PLANS.md" }`
- `agents_snippet.md` — the text dropped into `AGENTS.md`
- `files/` — tree of files copied to repo root respecting `target` paths

Install metadata is recorded in `.agent/promptkit/registry.json` (per repo). `AGENTS.md` is updated inside a managed block `<!-- promptkit:start --> ... <!-- promptkit:end -->`, so multiple packs stay tidy.

## Built-in pack: execplan

- Adds the ExecPlans rule to `AGENTS.md`.
- Writes `.agent/PLANS.md` containing the full Codex ExecPlan spec (living-plan guidance, milestones, validation, etc.).

## Road to PyPI & npm

This repo is structured to publish both:

- PyPI: package name `promptkit` exposes the Python CLI (`promptkit`). Works with `uvx promptkit ...` once published.
- npm: package `promptkit` exposes the Node CLI (`promptkit`). Works with `npx promptkit ...`.

## Development notes

- Python package data lives in `src/promptkit_builtin_packs/` and is included via `MANIFEST.in`.
- Node CLI reads the same pack data from `src/promptkit_builtin_packs/` to stay in sync.
- Quality tools:
  - Make (recommended): `make lint`, `make format`, `make typecheck`, or `make all` (runs lint+typecheck). Requires `uvx` available and `npm install` for JS dev deps.
  - Python direct: `uvx ruff check .`, `uvx black .`, `uvx mypy src` (deps in `optional-dependencies.dev`).
  - Node direct: `npm run lint`, `npm run format`, `npm run typecheck`.
