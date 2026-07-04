---
name: generate-pyproject
description: Use this skill when the user asks to create, generate, update, or regenerate a pyproject.toml (or requirements.txt) for this project by analyzing its source files for dependencies. Trigger phrases include "create a toml file for this project", "generate pyproject.toml", "make a requirements file", "pin our dependencies", "what packages does this project actually need".
---

# Generate pyproject.toml from project analysis

Scans this project's Python source for third-party imports, cross-references them
against what's actually installed in the local venv, and writes or updates
`pyproject.toml` with dependency versions pinned to what's really installed —
never guessed.

## Steps

1. **Find the venv.** Look for `venv/` or `.venv/` at the project root (per
   `CLAUDE.md`, this project uses `venv/`). If neither exists, stop and ask the
   user how dependencies should be resolved instead of guessing.

2. **Find source files**, excluding the venv and caches:
   `find . -name "*.py" -not -path "*/venv/*" -not -path "*/.venv/*" -not -path "*/__pycache__/*"`

3. **Extract top-level imports** (`import x`, `from x import ...`) from those
   files. Drop anything that's a standard-library module (Python's
   `sys.stdlib_module_names`) or a local module belonging to this project.

4. **Resolve each remaining import to an installed distribution + version**
   using the venv's pip, e.g. `venv/bin/pip show <name>`. Import names don't
   always match distribution names (`yaml` → `PyYAML`, `PIL` → `pillow`) — if
   a direct lookup fails, check `venv/bin/pip list --format=freeze` for the
   likely match.

5. **Cross-check with `venv/bin/pip list --format=freeze`** for packages
   installed but never directly imported (e.g. `uvicorn`, used only via the
   CLI/`fastapi dev`). Ask the user whether to include these before adding
   them.

6. **If `pyproject.toml` already exists**, read it first and only update the
   dependency list — preserve existing `[build-system]`, `[project]`
   metadata, and any other sections untouched.

7. **If it doesn't exist**, create a minimal one: `[project]` with `name`
   (from the directory name), `version = "0.1.0"`, `requires-python` (from
   the venv's Python version), and the pinned `dependencies` list. Don't add
   a `[build-system]` table unless asked for one or the project needs to be
   pip-installable.

8. **Show the proposed file/diff before writing** — this is project
   configuration, not a throwaway file.

9. **After writing**, tell the user versions were pinned to what's currently
   installed in `venv/`, and that re-running this skill after adding new
   imports or upgrading packages will keep it in sync.

## Rules

- Never invent version numbers — always derive them from the installed venv.
- Never list the project's own package as a dependency of itself.
- Ask before adding packages that were found installed but not directly
  imported anywhere.
