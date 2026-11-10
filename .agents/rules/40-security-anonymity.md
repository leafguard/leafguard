---
activation: always_on
description: Anonymity, secrets and upload-safety rules (hard constraints)
---
# Security and anonymity (hard constraints)

## Anonymity: disclosing the college name means disqualification
- NEVER write the college or institute name, logos, campus, staff names, student IDs or personal emails anywhere: code, comments, README, docs, commit messages, branch names, test data, image EXIF, notebooks, screenshots.
- Use only neutral team handles. Git identity is the neutral handle plus a no-reply email.
- Banned words live in a local file `.banned_terms.txt` (git-ignored, never committed). Run `python scripts/anonymity_audit.py` before every commit and release and fix every hit.
- Screenshots and images: strip metadata; no ID cards, uniforms, logos or faces.

## Secrets
- No tokens, keys or passwords in code, notebooks, docs or history. Use env vars locally and GitHub/HF secrets in CI.
- `.env`, `.banned_terms.txt`, datasets, `.venv/`, `__pycache__/` stay in `.gitignore`.
- If a secret is ever committed: stop, tell the team, rotate the secret. Deleting the file is not enough.

## Uploads are hostile
- Limits: 8 MB bytes, pixel cap against decompression bombs, minimum 100 px, real decode required.
- No uploaded data is written to disk or stored. The README privacy section says so.
- Rate limiting is a documented roadmap item unless explicitly requested.

## Advice safety
- Advice comes only from `advisory.json` entries that carry a `source` (title, url, retrieved date).
- Never write chemical names or doses. For chemical control: "Confirm product and dose with your local KVK or agriculture officer and follow the label."
- Every result shows a disclaimer in the selected language.
- Never machine-translate Hindi or Marathi and mark it reviewed. Keep `"reviewed": false` until a native speaker checks it.
