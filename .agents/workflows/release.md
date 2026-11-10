---
description: Prepare release notes and the deployment log entry AFTER the human has deployed
---
1. Ask the human to confirm the deploy finished with ALL PASSED and to paste the row printed by `scripts/deploy.py`.
2. Ask for the MEASURED numbers (lab accuracy, field accuracy, macro F1, latency). Never fill them in yourself.
3. Add the entry to `docs/DEPLOYMENTS.md` and propose a docs commit.
4. Draft release notes for the tag (what changed, measured numbers, known issues). Print the tag commands for the HUMAN to run: `git tag -a <tag> -m "<msg>"` and `git push origin <tag>`. Do not run them.
