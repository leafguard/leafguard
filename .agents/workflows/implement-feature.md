---
description: Implement one approved task in small verified steps
---
1. Confirm the approved plan. If none exists, run /plan-phase first.
2. Create a branch `feat/<short-name>` (or `fix/` or `docs/`).
3. Write or update the test first when behaviour changes, then implement the smallest change that passes it.
4. Run `pytest -q` and, if relevant, start the server and exercise the feature with curl or the browser. Show me the real output.
5. Run `python scripts/anonymity_audit.py` and fix any hit.
6. Update docs if behaviour, endpoints or setup changed.
7. Propose a conventional commit message and a pull request description (what, why, how tested).
8. Finish with "WHAT TO UNDERSTAND": 3 to 5 plain sentences and the key concepts, so a teammate can explain it in a viva.
Do not add dependencies or extra features that were not approved.
