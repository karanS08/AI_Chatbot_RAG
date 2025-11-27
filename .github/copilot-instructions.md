## Quick orientation for AI coding agents

This repo implements a Flask-based RAG chatbot focused on sugarcane farming. The UI is a mobile-first single-page app in `templates/index.html`. The server entrypoint is `app.py` which exposes the HTTP API and integrates with Google Gemini (via `google-genai`).

Keep this short — follow these repo-specific notes when editing, testing or extending code.

### Key files
- `app.py` — main Flask app and all routes: `/`, `/upload`, `/ask`, `/scan-image`, `/classify-plant`, `/webhook`, `/health`.
- `templates/index.html` — front-end UI and client-side logic (language selector, voice, image handling).
- `knowledge_base/` — content used by the RAG store (documents and reference plant images). Place new docs in the proper subfolder (e.g., `diseases/`, `sugarcane/`).
- `uploads/` — runtime uploads (gitignored). The server saves uploaded files here and also attempts to upload them into the Gemini file search store.
- `requirements.txt`, `Procfile`, `render.yaml`, `runtime.txt` — deployment + dependency definitions (Render.com ready).
- `test_*.py`, `requestss.py`, and small helper scripts — local integration tests that assume the server runs on `PORT` (default 5000).

### How the system is wired (big picture)
- Frontend (`index.html`) talks to Flask endpoints for RAG (`/ask`), image analysis (`/scan-image`), plant classification (`/classify-plant`), uploads (`/upload`), and webhooks (`/webhook`).
- `app.py` keeps a single Gemini client instance (`genai.Client`) using `GOOGLE_API_KEY`. It creates/uses a file-search store for RAG (calls: `client.file_search_stores.create()` and `file_search_stores.upload_to_file_search_store`).
- Image endpoints attach image bytes directly to Gemini Vision calls (parts with inline blobs). `/scan-image` expects the model to return JSON only (the code extracts JSON blocks from the model output).

### Environment & run commands (developer workflow)
- Required env: `GOOGLE_API_KEY`. Optional: `FLASK_ENV`, `FLASK_DEBUG`, `PORT`, `WEBHOOK_VERIFY_TOKEN`.
- Local dev run: `python app.py` (app is configured to listen on `PORT` or 5000). For production or to mimic Render: `gunicorn --bind 0.0.0.0:5000 --workers 2 --timeout 120 app:app`.
- Install deps: `pip install -r requirements.txt` (project targets Python 3.11 as per `runtime.txt`).
- Tests: many helper tests/scripts post to the running server (e.g., `test_classify_plant.py`); start the server first, then run test scripts.

### Project-specific conventions and patterns
- Language handling: `AGRICULTURAL_INSTRUCTIONS` in `app.py` contains per-language system prompts. When adding a language, update both `app.py` and `templates/index.html` (language selector + `languageCodes` in JS).
- Image & document validation: `allowed_file()` enforces extensions; `MAX_CONTENT_LENGTH` is 50MB (documents) and images are further constrained in frontend UX to ~10MB.
- Model usage pattern: prefer `client.models.generate_content` with `types.Content(parts=[...])` when sending images/refs. For RAG, include the file-search tool by name (`FileSearch(file_search_store_names=[store.name])`). Avoid changing the model name without reason — tests expect the existing calls.
- Output parsing: many endpoints expect the model to emit pure JSON. Code scans for fenced ```json blocks and falls back to raw text parsing. When editing, preserve the JSON-only contract for `/scan-image` and `/classify-plant`.

### Integration points & external deps
- Google Gemini (`google-genai` package) — used heavily for text + vision + file-search. Keep `google-genai==1.51.0` (requirements pin). Changes to model invocation must preserve the `types.GenerateContentConfig` usage.
- Deployment: Render (blueprint via `render.yaml`). `Procfile` and `runtime.txt` are already present.

### Fast attention items / gotchas (do this first)
1. app.py currently contains corrupted/invalid tokens near the JSON fallback and at the bottom `__main__` guard. If you plan to run tests or start the app, fix these obvious syntax problems first. Look for the literal tokens like `⚠️ Severity: unknown` and duplicated `app.run` calls near file end — these break import/run.
2. The code assumes `GOOGLE_API_KEY` exists. If missing, RAG endpoints return errors or the `/health` endpoint shows unhealthy. For local dev, set this env var to enable full behavior (or mock the client in tests).
3. The image endpoints expect the model answer to be parsable as JSON. When editing prompts or schemas, keep output strict (the frontend, tests and downstream code rely on predictable keys such as `diagnosis`, `recommendations`, `confidence`, `classification`).

### Concrete examples to reference when editing
- To add language-specific instructions: edit `AGRICULTURAL_INSTRUCTIONS` in `app.py` AND add the language option in `templates/index.html` and `translations` (JS).
- To see how uploads are processed: follow `/upload` in `app.py` — files are saved to `uploads/` and then `upload_file_to_store()` is called.
- To add a new endpoint that calls Gemini with files/images: mimic the pattern in `/scan-image` and `/classify-plant` (use `types.Part(inline_data=types.Blob(...))`).

### Tests & debugging tips
- Start the app (fix the syntax corruption) then run `python test_classify_plant.py --image path/to/image.jpg` to validate the vision/classification flow. Use the other helper scripts in the repo for RAG/webhook testing.
- When debugging model failures, capture `resp.text` (model raw text) — the code already logs/carries `raw_text` in several endpoints.

If anything in these notes is unclear or you want the instructions to bias toward safer editing (e.g. automatic unit tests or a template PR), tell me which preference and I will iterate this file.
