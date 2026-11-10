---
description: Full anonymity audit of repo, history, docs and assets
---
1. Run `python scripts/anonymity_audit.py` (reads the local `.banned_terms.txt`). Report every hit with file and line.
2. Also check: `git log --format='%an %ae %cn %ce' | sort -u` shows only neutral identities.
3. Search notebooks in `training/` (including saved outputs and metadata) and `docs/` for names, emails and paths like `C:\Users\<name>`.
4. List image files in `docs/` and `static/` and check their metadata (`exiftool` or Pillow) for author or location fields; strip any found.
5. Check README, slides text, tech note and PDF metadata for the institute name.
6. Report PASS or FAIL with a fix list. Do not edit history yourself; tell me what to do.
