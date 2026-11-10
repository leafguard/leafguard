---
activation: always_on
description: Core hackathon working style for LeafGuard
---
# Hackathon core rules

## Scope discipline
- Follow `docs/IMPLEMENTATION_PLAN.md` task by task. Stop at every **HUMAN** block and say what the human must do.
- Features are tagged MUST / SHOULD / COULD in docs/PHASES.md. Never start a SHOULD or COULD while a MUST is unfinished.
- Build the smallest version that works end to end, then improve. Prefer a thin working slice over a complete layer.
- If a request would add a new library, service, framework or file type, ask first and offer the cheaper alternative.

## Code style (judges read this)
- Readable over clever: short functions (aim under 30 lines), clear names, early returns, no metaprogramming.
- Type hints on every function signature. One-line docstring saying WHAT and, if not obvious, WHY.
- Comments explain WHY (e.g. "EXIF: phone photos are stored sideways"), not what the line does.
- Keep each file under about 150 lines. If larger, propose a split; do not silently refactor.
- No dead code, no commented-out blocks, no TODOs without an owner and date.
- Constants (thresholds, limits) live at the top of the file with a comment saying how they were tuned.

## Honesty
- Never fabricate accuracy, latency, dataset sizes, citations or URLs. Use placeholders like `<MEASURED: field accuracy>` until measured.
- When something fails, report the real error and its cause. Do not hide failures by loosening tests.

## Definition of done (every task)
1. It runs locally with the documented command.
2. A test or script proves it (add or update a pytest test when behaviour changes).
3. `pytest -q` passes, with no new warnings you cannot explain.
4. Docs updated if behaviour, endpoints or setup changed.
5. A conventional commit message is proposed. No secrets, no college name.
6. You gave the "WHAT TO UNDERSTAND" note.

## Planning
For anything touching more than one file: produce a plan (files to change, risks, test approach), wait for approval, then implement in small steps and verify each step.
