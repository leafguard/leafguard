# Antigravity setup kit for LeafGuard (manual deployment edition)

The kit makes Google Antigravity generate hackathon-suited code (small, readable, tested, honest, anonymous),
follow a written task plan, and STOP whenever a human must act (training, translations, deploys).
You deploy by hand at fixed checkpoints; the agent only tells you when you are ready.

## 1. Install the kit (10 minutes)
1. Copy everything in this folder INTO the root of your `leafguard` repo, except this file. Hidden folders
   `.agents/` and `.github/` must be copied too. Merge `gitignore-additions.txt` into your `.gitignore`.
2. Open the repo in Antigravity. It reads `AGENTS.md` and rule files in `.agents/rules/`.
   Open its Customizations / Rules panel and confirm 6 rules and 7 workflows appear.
   - If they do not appear, your version may use the singular folder: rename `.agents` to `.agent`.
   - If `AGENTS.md` is not picked up, copy it to `GEMINI.md` in the repo root.
   - Antigravity changes often; check https://antigravity.google/docs/overview if a menu looks different.
3. Neutral git identity: `git config user.name "<handle>"` and `git config user.email "<noreply email>"`.
4. Create `.banned_terms.txt` (college name, short forms, city, staff names; one per line). It is git-ignored.
5. Follow "One-time setup" in `docs/MANUAL_DEPLOY.md` (Hugging Face Space and the `hf` git remote).

## 2. How the agent moves
- `docs/IMPLEMENTATION_PLAN.md` is its map: milestones M0 to M8, each with tasks, specs and acceptance checks.
- `/next-task` finds the next unfinished task and proposes a plan. You approve; it implements (`/implement-feature`),
  tests, and ticks the box.
- At every **HUMAN** block it stops and lists what you must do (Kaggle run, writing advice from sources, translations,
  phone tests, deploys).
- `/pre-deploy` gives a PASS/FAIL report and says "READY FOR DEPLOY CHECKPOINT Dx". It never deploys.
- `/daily-wrap` ends each day with a progress summary and a stumble list to study.
- `/anonymity-audit` before every day's last push. `/release` helps with notes after you deploy.

## 3. When you deploy (you, manually)
Checkpoints D1 to D7 with dates and conditions are in `docs/MANUAL_DEPLOY.md`. In short:
D1 today (skeleton), D2 Tue evening (API), D3 Wed evening (full UI, real model), D4 Thu (freeze),
D5 Fri only if needed, D6 Sat before noon (final), then critical fixes only.
Command each time: `python scripts/deploy.py --url https://<handle>-leafguard.hf.space`.

## 4. Kick-off prompt for Antigravity (paste at the start of M0)
```
Read AGENTS.md, then docs/IMPLEMENTATION_PLAN.md section M0 only. Follow /next-task: show me a plan for T0.1,
wait for my approval, implement it, run its acceptance check, tick the box in the plan, and move to T0.2 the same way.
Stop at the HUMAN block H0 and tell me what I must do. Do not deploy anything.
```
For later milestones just say: `/next-task`.

## 5. Caveats
- The untested pieces: `scripts/make_dummy_model.py` and the optional `--record` option of `deploy.py` were written
  without a network to test them here. The plan's task T2.1 tells the agent to verify the dummy model. If `--record`
  fails, ignore it; the deploy itself does not depend on it.
- Free hosting limits and Antigravity features change; re-check them before relying on them.
- Review all generated code. Agents can invent library versions, URLs, sources and numbers; the rules forbid it,
  but you are the final check.
