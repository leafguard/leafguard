# LeafGuard: project rules for the coding agent

LeafGuard is a hackathon web app (Srujan 2026, problem AI-05, crop disease identification).
A farmer photographs a leaf; the app returns the top-3 likely diseases, a confidence status and
short sourced advice in English, Hindi and Marathi. It runs on CPU. Judges will open the live URL,
read this GitHub repo, and question the team about every line. Optimise for that.

## The plan is the source of truth
- Follow `docs/IMPLEMENTATION_PLAN.md`. Read ONLY the current milestone section, not the whole file.
- Work on ONE task at a time, in order. When a task's acceptance criteria pass, tick its checkbox in the plan.
- When you reach a block marked **HUMAN**, STOP and tell me exactly what I must do. Never skip it or fake it.
- Do not start a later milestone while an earlier one has unticked MUST tasks.
- Deployment is MANUAL and done only by a human (see `docs/MANUAL_DEPLOY.md`). You never deploy, never push to the
  Hugging Face remote, never run `scripts/deploy.py`. You only prepare for deployment and say when it is time.

## Priorities (in this order)
1. A working, deployed, demo-able product beats any extra feature.
2. Code the team can explain beats clever code. Plain, boring, readable Python and JavaScript.
3. Honest numbers and honest limits beat impressive claims.
4. Small, frequent, working commits. Never leave `main` broken.

## Fixed stack (do not change without asking)
- Training: PyTorch + torchvision MobileNetV3-Large, ONLY on Kaggle/Colab, never locally.
- Serving: Python 3.11, FastAPI, Uvicorn, ONNX Runtime (CPU), Pillow, NumPy. No PyTorch at runtime.
- Frontend: plain HTML/CSS/vanilla JS in `static/`, served by FastAPI. No build step, no framework.
- Storage: JSON files in the repo + browser localStorage. No database.
- Hosting: Hugging Face Spaces (Docker, port 7860). Code on public GitHub. Manual deploys.

## Folder map
```
app/main.py        routes, validation, status bands
app/inference.py   preprocess + ONNX predict + blur score
app/advisory.py    label -> advice lookup (EN/HI/MR)
app/version.py     reads app/version.json for /version (written only at deploy time, git-ignored)
app/data/          labels.json, advisory.json
app/model/         leaf.onnx (Git LFS); MODEL_IS_DUMMY marker while a placeholder is used
static/            index.html app.js styles.css manifest.json
training/          Kaggle notebook with printed metrics
tests/             pytest tests + sample_images/ + fixtures/
scripts/           deploy.py (human only), smoke_test.py, check_advisory.py, anonymity_audit.py, ...
docs/              IMPLEMENTATION_PLAN.md, PHASES.md, MANUAL_DEPLOY.md, DEPLOYMENTS.md, TECH_NOTE.md
.agents/           rules and workflows for this agent
```

## Commands
- Run: `uvicorn app.main:app --reload --port 8000`
- Test: `pytest -q`
- Advice coverage: `python scripts/check_advisory.py`
- Anonymity: `python scripts/anonymity_audit.py`

## Non-negotiables (details in `.agents/rules/`)
- Preprocessing in `inference.py` must exactly match training (Resize 256, CenterCrop 224, ImageNet mean/std).
- Advice text is stored, sourced, reviewed text. NEVER generate advice, pesticide names or doses.
- The college/institute name must never appear anywhere (code, comments, commits, docs, metadata).
- No secrets in the repo. Use environment variables.
- Every upload is untrusted: size limit, real decode, pixel limit, clear 4xx errors, never a 500.
- Do not add dependencies, files or features that were not in the plan or asked for.

## Working style
- For any task bigger than one file, show a short plan first and wait for approval (use /plan-phase).
- After each task finish with "WHAT TO UNDERSTAND": 3 to 5 plain sentences on what changed and which concepts it
  uses, so a teammate can explain it in a viva. Name any trade-off.
- If something is unknown or unverified, say so. Never invent numbers, sources, versions or URLs.
