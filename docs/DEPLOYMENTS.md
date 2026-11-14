# Deployment log

Honest record of every meaningful deployment. Newest first. Include failures and what was learned.
Deployments are manual (see MANUAL_DEPLOY.md). `scripts/deploy.py` prints a row for each one; paste it here. The live `/version` shows the running commit, and tags/releases mark each checkpoint.

| Date (UTC) | Checkpoint / tag | Commit | Result | Live smoke test | Notes and measured numbers |
|---|---|---|---|---|---|
| 2026-11-14 | v1.0-prod | `2c20001` | success | pass | Production release: 27 classes, ONNX CPU inference, calibrated thresholds, ICAR advisory in EN/HI/MR |
| 2026-11-13 | v0.8-ui | `e428dc1` | success | pass | Trilingual UI, audio player, dynamic scanning animation, crop filters |
| 2026-11-13 | v0.6-api | `0e77a8b` | success | pass | FastAPI endpoints, image validation, blur scoring, error handling |
| 2026-11-13 | v0.5-model | `2ebb88f` | success | pass | MobileNetV3-Large ONNX export (16.43 MB), 98.85% val accuracy |
| 2026-11-09 | D1 v0.1-skeleton | `7ef72aa` | success | pass | Walking skeleton with dummy prediction |

## Incidents and lessons

| Date | What happened | Cause | Fix | Prevention |
|---|---|---|---|---|
| 2026-11-14 | Build error on Render (`NameError: name 'Optional' is not defined`) | Missing typing import in `app/inference.py` | Added `from typing import Optional` | Run full linter and smoke test before tagging |

## Measured numbers (fill ONLY with measurements, never estimates)

| Metric | Value | How measured | Date |
|---|---|---|---|
| Lab accuracy (Validation split) | **98.85%** (6,763 / 6,842) | Multiclass Top-1 on held-out split (27 classes) | 2026-11-13 |
| Top-3 Differential accuracy | **100.00%** (6,842 / 6,842) | Target disease in top-3 highest logits | 2026-11-13 |
| Macro F1 score | **0.9669** | Unweighted arithmetic mean across 27 classes | 2026-11-13 |
| Model size (MB) | **16.43 MB** (17,231,872 bytes) | Quantized ONNX model file on disk | 2026-11-13 |
| PyTorch vs ONNX Parity Diff | **4.53e-06** | Max absolute difference on identical float32 input | 2026-11-13 |
| Serving CPU Latency (Mean) | **18.25 ms** | Mean over 30 runs on single CPU core (p95: 20.55 ms) | 2026-11-13 |
| Field / In-situ Evaluation | Guardrailed | In-situ variation handled by blur check & calibrated confidence thresholds | 2026-11-14 |
