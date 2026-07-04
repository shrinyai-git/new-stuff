# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this is

A minimal single-file FastAPI application (`main.py`). There is no package structure, no test suite, no requirements file, and no README yet — everything currently lives in `main.py`.

## Development

Dependencies are installed in a local `venv/` (Python 3.11, FastAPI 0.139.0, Uvicorn 0.49.0). Activate it before running anything:

```
source venv/bin/activate
```

Run the dev server:

```
fastapi dev main.py
```

or directly with uvicorn:

```
uvicorn main:app --reload
```

There is no `requirements.txt` or `pyproject.toml` — if you add dependencies, install them into `venv` and create one of these files to pin them.

## Architecture

`main.py` defines a single FastAPI `app` instance with route handlers declared directly as decorated functions (`@app.get(...)`). There is currently no routing module, no models/schemas, and no separation between route handlers and business logic — e.g. `hello_world()` is a plain helper called from the `/hello` route handler. As the app grows, watch for where this flat structure needs to be split out.
