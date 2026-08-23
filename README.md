# cra-demo

Fresh demo repository for **Code Review Assistant**.

Use this repo to verify:

1. PR reviews (scanners + LLM + impact callers)
2. Dashboard shows **PR title** (not only commit SHA)
3. Default-branch **repo scans** and the Scans tab

Full step-by-step: see [`TEST_STEPS.md`](./TEST_STEPS.md) in this folder (also copied under CRA root docs below if linked).

## Layout

| File | Purpose |
|------|---------|
| `app.py` | Core logic with intentional SQL injection (scanner + LLM target) |
| `api.py` | Imports `get_user` from `app` — reverse-import **impact** caller |
| `helpers.py` | Weak sanitizer used by `app.py` |
| `db.py` | Fake query executor |
| `config.py` | Placeholder config (keep clean on `main`) |
| `requirements.txt` | Minimal Python deps list |

## Quick idea

1. Put `api.py` on **main** first.
2. Open a PR that only changes `app.py`.
3. Worker should log impact caller `api.py` and post a PR comment.
4. Dashboard Reviews row should show the **PR title**.
# phase-e 2026-08-23T08:00:11+00:00
