# Production Deployment & Operations Runbook

This document details the repeatable deployment and staging protocol for LeafGuard on containerized cloud infrastructure.

Live deployments can be independently verified via `/version` (matching the current git commit SHA), [docs/DEPLOYMENTS.md](DEPLOYMENTS.md), release git tags, and GitHub Deployments.

---

## 1. Environment & Remote Setup
1. **Container Registry / Host**: Cloud host (Render / Hugging Face Docker Space), port 7860.
2. **Git LFS Configuration**:
   ```bash
   git lfs install
   git lfs track "*.onnx"
   ```
3. **Anonymity & Policy Compliance**:
   Ensure `.banned_terms.txt` exists locally for the anonymity audit prior to every deployment release.

---

## 2. Standard Deployment Command
```bash
git switch main && git pull
python scripts/deploy.py --url https://<deployment-url> [--allow-dummy] [--record]
```

### Automation Sequence:
1. **Pre-flight Integrity:** Verifies working tree is clean and local `main` matches `origin/main`.
2. **Automated Test Gate:** Executes complete pytest suite, advisory coverage check, and zero-leak anonymity audit.
3. **Version Stamping:** Generates `app/version.json` with commit SHA, timestamp, and deployment ID.
4. **Container Build & Sync:** Deploys Docker container and awaits healthy container startup.
5. **Post-Deploy Smoke Test:** Queries `/health`, `/version`, and executes live `/predict` smoke validation.
6. **Audit Record:** Logs release metrics into [docs/DEPLOYMENTS.md](DEPLOYMENTS.md).

---

## 3. Deployment Checkpoints & Release History

| Checkpoint | Target Phase | Release Gate Criteria | Target Tag |
|---|---|---|---|
| **D1** | Walking Skeleton | Base FastAPI service running in Docker container, initial CI tests green. | `v0.1-skeleton` |
| **D2** | API & Hardening | Production ONNX inference pipeline, error bands, and payload security. | `v0.6-api` |
| **D3** | Full UI & Advisory | Multilingual ICAR advisory knowledge base (EN/HI/MR) with responsive web UI. | `v0.8-ui` |
| **D4** | Field Tuning & Freeze | Calibrated confidence bands ($0.40 / 0.20$), Bayesian crop gating, feature freeze. | `v0.9-freeze` |
| **D5** | Submission Pack | Comprehensive README, technical evaluation note, and empirical verification. | `v1.0-rc` |
| **D6** | Production Release | Final end-to-end verified release for competition evaluation and live testing. | `v1.0-round1` |

---

## 4. Operational Safety Guidelines
- Never deploy without automated test pass (`pytest -q`), zero missing advisory entries, and clean anonymity audit.
- After feature freeze (D4), only critical bug fixes are merged.
- Keep the live health monitor active on `/health` to prevent container idling.

---

## 5. Troubleshooting & Rollback Procedures

| Issue | Root Cause & Resolution |
|---|---|
| **Git LFS File Size Error** | Verify `git lfs track "*.onnx"` was executed before committing binary weights. Use `git lfs ls-files` to inspect tracked blobs. |
| **Container Build Failure** | Inspect build logs; confirm Dockerfile exposes port 7860 and dependencies install cleanly under Python 3.11. |
| **Version Hash Mismatch** | Container build is still in progress; wait for Docker build cache to complete or rerun smoke test via `python scripts/smoke_test.py`. |
| **Emergency Rollback** | In the event of a production regression, revert via `git revert <commit-sha>`, push to main, and rerun deployment script. Never force-push main. |
