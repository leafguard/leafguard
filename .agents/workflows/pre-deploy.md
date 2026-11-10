---
description: Readiness report before a human deploys (never deploys itself)
---
1. State which deploy checkpoint (D1 to D6, see `docs/MANUAL_DEPLOY.md`) we are preparing and read its conditions.
2. Run `pytest -q`; all tests must pass.
3. Run `python scripts/check_advisory.py` (once advisory data exists); no MISSING, EMPTY, NO SOURCE or placeholder lines.
4. Run `python scripts/anonymity_audit.py`; zero hits.
5. Start locally: `uvicorn app.main:app --port 8000`. Check `/health`, `/version`, and `/predict` with `tests/sample_images/` using curl. Show the real output.
6. Check the Dockerfile (builds if Docker is available; port 7860; non-root; no secrets) and that README still starts with the Hugging Face front matter (`sdk: docker`, `app_port: 7860`).
7. Check `git status` is clean, branch is main, and main is pushed to origin. Check no dataset, `.env`, `.banned_terms.txt` or `app/version.json` is tracked.
8. Check `app/model/MODEL_IS_DUMMY`: allowed only for D1 and D2.
9. Output a PASS/FAIL table. If all PASS say: "READY FOR DEPLOY CHECKPOINT Dx" and print the human commands from `docs/MANUAL_DEPLOY.md`. If any FAIL, stop and explain. You must not run the deploy.
