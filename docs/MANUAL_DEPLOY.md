# Manual deployment runbook (human only)

Nothing deploys by itself. YOU deploy at the checkpoints below, after the coding agent reports
"READY FOR DEPLOY CHECKPOINT Dx". Judges can still verify every deployment: the live `/version` shows the exact
commit, `docs/DEPLOYMENTS.md` logs each one, tags/releases mark them, and (optionally) GitHub's Deployments panel lists them.

## One-time setup (do before D1, 15 minutes)
1. Hugging Face (neutral account): New Space, SDK Docker, public, name `leafguard`. Create a write access token
   (Settings, Access Tokens). Never paste the token in chat, code or docs.
2. In your repo folder: `git remote add hf https://huggingface.co/spaces/<handle>/leafguard`
   (first push asks for username and the token as password; your credential manager remembers it).
3. `git lfs install` and `git lfs track "*.onnx"` (before the model is first committed).
4. Create `.banned_terms.txt` (college name, short forms, city, staff names; one per line). It is git-ignored.
5. Optional, for the Deployments panel: install GitHub CLI (`gh auth login`) and use `--record` below.
6. Your Space URL is `https://<handle>-leafguard.hf.space`.

## The deploy command (same every time)
```
git switch main && git pull
python scripts/deploy.py --url https://<handle>-leafguard.hf.space [--allow-dummy] [--record]
```
What it does: checks you are on a clean, pushed `main`; runs tests, advisory check and anonymity audit; stamps
`app/version.json` on a TEMPORARY branch; force-pushes that to the Space; waits for the Space to rebuild until the live
`/version` equals your commit; smoke-tests the live site; prints a row for `docs/DEPLOYMENTS.md`. `main` is never changed.
Expect the Space build to take a few minutes. If it prints FAILED, read the message, fix on a branch, merge, deploy again.

After a successful deploy (every time)
1. Open the live URL on your phone over mobile data and scan once.
2. Paste the printed row into `docs/DEPLOYMENTS.md`; commit and push (docs-only; no redeploy needed).
3. Tag the milestone: `git tag -a v0.1-skeleton -m "walking skeleton live"` then `git push origin v0.1-skeleton`.

## Deploy checkpoints: WHEN to deploy

| ID | When | Trigger (all must be true) | Flags | Tag |
|---|---|---|---|---|
| D1 | Mon 9 Nov, tonight | M0 done: skeleton runs locally, tests green, Dockerfile valid | `--allow-dummy` | `v0.1-skeleton` |
| D2 | Tue 10 Nov evening | M2 done: real inference code and API validation, tests green (placeholder or real model) | `--allow-dummy` if the model is not ready | `v0.6-api` |
| D3 | Wed 11 Nov evening | M3 and M4 done: advice and full UI work end to end with the REAL model | none | `v0.8-ui` |
| D4 | Thu 12 Nov | M5 done: thresholds tuned on field photos, FEATURE FREEZE | none | `v0.9-freeze` |
| D5 | Fri 13 Nov, only if needed | M6 fixes found in the final review (README front matter, bug fix) | none | `v1.0-rc` |
| D6 | Sat 14 Nov, before 12:00 | M7: final candidate, full pre-deploy PASS, submission-day check | none | `v1.0-round1` |
| D7+ | 15 to 25 Nov | CRITICAL fixes only, after a branch test and pre-deploy PASS | none | `v1.0.x` |

Rules for deploying
- Never deploy with failing tests, an anonymity hit, or a dummy model (except D1 and D2).
- Do not deploy late at night or in a hurry. If D4 slips, deploy D4 on Friday morning and cut D5; never skip D6.
- Deploy at least once a day from Monday on, so the live site always runs recent code and the history shows steady work.
- After D4 (freeze), change only what is broken. Never change the Space name or URL.
- Keep the Render backup deployment (see `docs/PHASES.md`, Phase 5) in sync only at D4 and D6 (same code, manual).

## If something goes wrong
| Symptom | Do this |
|---|---|
| Push to the Space is rejected for a large file | Confirm `git lfs track "*.onnx"` was done before committing the model; if not, ask for help migrating (`git lfs migrate`) before deploying |
| Build fails on the Space | Open the Space's Logs tab; confirm README front matter and `app_port: 7860`; fix on a branch; redeploy |
| Smoke test says wrong sha after a long wait | Space still building or the push failed; open the Space page and check build status, then rerun `python scripts/smoke_test.py` with `BASE_URL` and `EXPECTED_SHA` set |
| Live site is broken after a deploy | Undo the bad change with `git revert <bad-commit>` on main, push to origin, then deploy again (never force-push main) |
| Space asleep | Visit the URL; set up the uptime monitor on `/health` |
