---
activation: always_on
description: Git discipline and the MANUAL deployment process
---
# Git and deployment rules

## Git
- `main` is always deployable. Work on `feat/<name>`, `fix/<name>`, `docs/<name>` and merge through a pull request (even solo) so history shows reviewed work.
- Conventional commits: `feat:`, `fix:`, `docs:`, `test:`, `chore:`, `ci:`. One logical change per commit, imperative subject under 72 characters.
- Never force-push `main`. Never rewrite published history. Never commit datasets, `.venv`, `.env`, `.banned_terms.txt` or `app/version.json`.
- `*.onnx` is tracked with Git LFS (`git lfs track "*.onnx"` BEFORE the first commit of the model).
- Tags mark milestones: `v0.1-skeleton`, `v0.5-model`, `v0.8-ui`, `v0.9-freeze`, `v1.0-round1`. The human creates tags after a successful deploy.

## Deployment is MANUAL and human-only
- You (the agent) must NEVER: run `scripts/deploy.py`, push to the `hf` remote, create or edit anything on Hugging Face, or tag a release.
- Your job is to make main READY: tests green, advisory check green, anonymity audit clean, Dockerfile valid, README front matter intact.
- Use `/pre-deploy` to produce a PASS/FAIL report. If PASS, tell the human "READY FOR DEPLOY CHECKPOINT Dx" and show the exact commands from `docs/MANUAL_DEPLOY.md`. Then stop.
- Deploy checkpoints (D1 to D6) and their conditions are listed in `docs/MANUAL_DEPLOY.md`. Do not suggest deploying outside them unless the live site is broken.
- A deployment is VALID only when `scripts/deploy.py` finishes with ALL PASSED: live `/version` sha equals the commit, `/health` is ok, the sample photo returns 200 with `top`, and bad inputs return 400/413.
- Never claim something is deployed or live unless the human confirms it.
- Dockerfile rules: port 7860, non-root user uid 1000, no secrets copied, stateless.
- After feature freeze (tag `v0.9-freeze`) only critical bug fixes. Never change the public URL.
