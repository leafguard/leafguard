# Phases and gates (summary; the task detail is in IMPLEMENTATION_PLAN.md)

Priority tags: MUST, SHOULD, COULD. A phase gate must be true before the next phase starts.
Deployment is manual; checkpoints D1 to D7 and their conditions are in `MANUAL_DEPLOY.md`.

| Phase | Date | Goal | Deploy | Tag |
|---|---|---|---|---|
| M0 Walking skeleton | Mon 9 Nov | Repo, rules, fixed-response API, simple page, Dockerfile | D1 (dummy allowed) | `v0.1-skeleton` |
| M1 Model (Kaggle, parallel) | 9 to 10 Nov | `leaf.onnx`, labels, metrics, parity passed | none | `v0.5-model` |
| M2 Inference and API | Tue 10 Nov | Real predictions, validation, bands, tests | D2 | `v0.6-api` |
| M3 Advisory KB | 10 to 11 Nov | Sourced EN advice, reviewed HI and MR | none | none |
| M4 Frontend | Wed 11 Nov | Full phone UI, 3 languages, voice, history | D3 (real model) | `v0.8-ui` |
| M5 Field test and freeze | Thu 12 Nov | Tune thresholds on real photos, freeze | D4 | `v0.9-freeze` |
| M6 Submission pack | Fri 13 Nov | README, tech note, slides, video, audits | D5 if needed | `v1.0-rc` |
| M7 Final release | Sat 14 Nov | Final test, deploy before noon, submit | D6 | `v1.0-round1` |
| M8 Judging | 15 to 25 Nov | Keep alive, critical fixes only | D7+ | `v1.0.x` |

## Gates
- **M0:** tests green; Dockerfile valid; `/version` works; anonymity audit clean; D1 live and tagged.
- **M1:** parity about 1e-4 or smaller; both lab and field numbers recorded (or `<NOT MEASURED>`); model under 25 MB, tracked by LFS.
- **M2:** all API error cases covered by tests; preprocessing reference test passes with the real model; latency measured.
- **M3:** `check_advisory.py` reports 0 problems; every entry sourced; no doses; native review done for hi and mr.
- **M4:** works on a real Android phone over mobile data; screenshots saved without metadata.
- **M5:** thresholds chosen with reasons; failure cases listed; uptime monitor and backup ready.
- **M6:** all submission files ready; two-person anonymity audit PASS.
- **M7:** release published; submission confirmation saved.

## What judges can verify
| Claim | Where |
|---|---|
| It is really deployed | Live URL; `/version` shows the exact commit; `docs/DEPLOYMENTS.md`; tags and releases; optional GitHub Deployments panel (`--record`) |
| Work was incremental and honest | Commit history, pull requests, tags |
| Tests exist and pass | Tests badge from Actions, `tests/` folder |
| Numbers are measured | Notebook outputs in `training/`, tables in `docs/TECH_NOTE.md`, `metrics.json` |
| Failures are handled | Incident table in `docs/DEPLOYMENTS.md` |

README badge: `![Tests](https://github.com/OWNER/REPO/actions/workflows/ci.yml/badge.svg)`
