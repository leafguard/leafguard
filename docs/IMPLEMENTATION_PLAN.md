# LeafGuard implementation plan (the coding agent follows this, task by task)

## How to use this file (agent)
- One task at a time, in order. Read ONLY the current milestone. Tick `[x]` when acceptance passes.
- Each task lists: **Files**, **Spec**, **Accept** (what must be true), **Commit** (suggested message).
- **HUMAN** blocks are things only a person can do (Kaggle, accounts, translations, deploys). STOP there and say exactly what is needed.
- Priority tags: MUST, SHOULD, COULD. Never start SHOULD/COULD while a MUST in the same or an earlier milestone is open.
- Anything marked `<NOT MEASURED>` stays that way until a human supplies a measurement.

## Global specifications (referenced by all tasks)

**Labels.** `app/data/labels.json` is a JSON list of class names in the exact training order, e.g. `"Tomato___Late_blight"`.
Class folder names are the labels. A class `"Not_a_leaf"` may exist (SHOULD).

**POST /predict** (multipart: `file`, `lang` in `en|hi|mr`, default `en`). Response 200:
```json
{
  "status": "confident",
  "blurry": false,
  "top": [
    {"label": "Tomato___Late_blight", "name": "Tomato - Late blight", "prob": 0.93},
    {"label": "Tomato___Early_blight", "name": "Tomato - Early blight", "prob": 0.05},
    {"label": "Tomato___healthy", "name": "Tomato - Healthy", "prob": 0.01}
  ],
  "advice": {
    "title": "Tomato - Late blight",
    "symptoms": ["..."], "actions": ["..."], "prevention": ["..."],
    "source": {"name": "...", "url": "...", "retrieved": "2026-11-11"},
    "disclaimer": "...", "reviewed": true
  }
}
```
`advice` is omitted when `status` is `unrecognised`. `name` falls back to the label if no advisory entry exists.
Errors: `{"detail": "<plain message>"}` with 400 (bad/too small/unreadable image), 413 (over 8 MB), 422 (FastAPI validation).

**Status bands** (constants in `app/main.py`): `CONF_OK = 0.70`, `CONF_LOW = 0.45`, `BLUR_MIN = 40.0`.
confident if top prob >= CONF_OK; uncertain if >= CONF_LOW; else unrecognised. Values are tuned in M5.

**Advisory JSON schema** (`app/data/advisory.json`), keyed by label:
```json
{
  "_disclaimer": {"en": "...", "hi": "...", "mr": "..."},
  "Tomato___Late_blight": {
    "name": {"en": "", "hi": "", "mr": ""},
    "symptoms": {"en": [], "hi": [], "mr": []},
    "actions": {"en": [], "hi": [], "mr": []},
    "prevention": {"en": [], "hi": [], "mr": []},
    "source": {"name": "", "url": "", "retrieved": ""},
    "reviewed": {"en": false, "hi": false, "mr": false}
  }
}
```
Placeholders start with `<NEEDS` (e.g. `"<NEEDS SOURCE>"`). Agents NEVER write real advice text; humans do (M3).

**Limits.** Upload max 8 MB; min shorter side 100 px; `Image.MAX_IMAGE_PIXELS = 50_000_000`; history 10 scans.

---

## M0: Walking skeleton (Mon 9 Nov) -> Deploy D1
Goal: the simplest possible app, live on the Space, with the whole pipeline proven.

- [x] **T0.1 (MUST) Project scaffold.** Files: `.gitignore` (use `gitignore-additions.txt`), `requirements.txt` (`fastapi`, `uvicorn[standard]`, `onnxruntime`, `pillow`, `numpy`, `python-multipart`), `requirements-dev.txt` (exists), `app/__init__.py`, `tests/__init__.py`, empty `tests/sample_images/`.
  Accept: `python -m venv .venv`, `pip install -r requirements.txt -r requirements-dev.txt` works on Python 3.11 or 3.12. Commit: `chore: project scaffold`.
- [x] **T0.2 (MUST) Placeholder labels.** `app/data/labels.json` with 3 labels: `["Tomato___Early_blight","Tomato___Late_blight","Tomato___healthy"]`. Commit: `chore: placeholder labels`.
- [x] **T0.3 (MUST) Skeleton API.** `app/main.py`: `/health` (`{"status":"ok","model":"dummy"}`), `/version` (via `app/version.py`; sha `"dev"` locally), `/predict` returning a FIXED response in the final shape (status `confident`, 3 top items, a short fake advice with `"reviewed": {"en": false, ...}`), and static mount of `static/` at `/`.
  Accept: `uvicorn app.main:app --port 8000` then curl `/health`, `/version`, `/predict` all return valid JSON. Commit: `feat: skeleton api`.
- [x] **T0.4 (MUST) Skeleton page.** `static/index.html` (+ minimal `app.js`): a file input, a button, and a `<pre>` showing the JSON from `/predict`.
  Accept: upload any image in the browser and see JSON. Commit: `feat: skeleton page`.
- [x] **T0.5 (MUST) Tests.** `tests/test_api.py` with `TestClient`: `/health` ok, `/version` has `sha`, `/predict` 200 with `top` and `status`.
  Accept: `pytest -q` green. Commit: `test: skeleton api tests`.
- [x] **T0.6 (MUST) Container and README.** `Dockerfile` exactly: `python:3.11-slim`, `WORKDIR /app`, copy `requirements.txt`, pip install `--no-cache-dir`, copy all, `useradd -m -u 1000 user`, `USER user`, `EXPOSE 7860`, `CMD uvicorn app.main:app --host 0.0.0.0 --port 7860`. `.dockerignore` (`.venv`, `.git`, `tests`, `datasets`, `__pycache__`). `README.md` starting with front matter `title: LeafGuard`, `sdk: docker`, `app_port: 7860`, then a short description, run commands, privacy line ("photos are not stored"), and a "Status: work in progress" note.
  Accept: if Docker exists, `docker build` and `docker run -p 8000:7860` serve the page. Commit: `chore: dockerfile and readme`.
- [x] **T0.7 (SHOULD) CI.** Keep `.github/workflows/ci.yml` (tests only). Accept: green run on GitHub. Commit: `ci: run tests`.
- **HUMAN H0:** create neutral GitHub and Hugging Face accounts; create the repo and the Space; add the `hf` remote; create `.banned_terms.txt`; set git identity; follow "One-time setup" in `docs/MANUAL_DEPLOY.md`.
- Agent: run `/pre-deploy` for **D1**. **HUMAN: deploy D1** (`--allow-dummy`), phone test, log it, tag `v0.1-skeleton`.

## M1: Model pipeline (parallel, ML lead; runs on Kaggle)
Goal: `leaf.onnx` + `labels.json` + honest metrics. The agent writes the notebook; humans run it.

- [x] **T1.1 (MUST) Training notebook** `training/train_kaggle.ipynb`, sections in order:
  1. Seeds (`random`, `numpy`, `torch`) and printed versions of python, torch, torchvision, onnxruntime.
  2. Data: `DATA` path variable; `ImageFolder` train/val; PRINT every class name with its image count and warn on any class under 100 images. Save `labels.json`.
  3. Transforms exactly as in `.agents/rules/30-ml-training.md` (train: RandomResizedCrop(224, scale 0.5-1), flip, rotation 20, ColorJitter(0.3,0.3,0.3,0.05), ToTensor, Normalize, RandomErasing(0.2); val: Resize(256), CenterCrop(224), ToTensor, Normalize).
  4. Model: `mobilenet_v3_large` ImageNet weights; replace `classifier[3]`; loss with `label_smoothing=0.1`.
  5. Phase A: freeze `model.features`, AdamW lr 1e-3, 3 epochs. Phase B: unfreeze, AdamW lr 1e-4, `CosineAnnealingLR(T_max=6)`, 6 epochs. Print train/val loss and accuracy each epoch; keep the best-val weights.
  6. Evaluation function reporting accuracy, macro F1, top-3 accuracy, per-class recall, confusion matrix (plot) for BOTH the PlantVillage val set AND a field set (folder `FIELD` with the same class folder names; skip gracefully if absent, printing "field set missing").
  7. Export: `model.eval().cpu()`, opset 17, input `input`, output `logits`, dynamic batch; parity check against PyTorch (print max abs difference; assert below 1e-3).
  8. Reference tensor: take `tests/sample_images/ref_leaf.jpg`, apply the VAL transform with torchvision, save `preproc_reference.npy` shape (1,3,224,224).
  9. Save `leaf.onnx`, `labels.json`, `preproc_reference.npy`, and a `metrics.json` with all numbers.
  Accept: notebook has no hard-coded absolute paths except the clearly marked `DATA`/`FIELD` variables. Commit: `feat: kaggle training notebook`.
- [x] **T1.2 (MUST) Tech note skeleton** `docs/TECH_NOTE.md` with the sections from the execution plan (problem and scope, data and licences, model, results table with `<NOT MEASURED>` cells for lab/field, serving, advisory, limitations, reproduce, future work). Commit: `docs: tech note skeleton`.
- **HUMAN H1:** pick the crop subset after reading the printed class counts (check coverage; PlantVillage soybean is healthy-only); run the notebook on Kaggle; build the field set (PlantDoc subset + own photos, 30 to 100); download `leaf.onnx`, `labels.json`, `preproc_reference.npy`, `metrics.json`; copy them into `app/model/`, `app/data/`, `tests/fixtures/`; commit the model with Git LFS; fill the numbers in `docs/TECH_NOTE.md`; save one clean sample photo as `tests/sample_images/ref_leaf.jpg`. Tag `v0.5-model` after committing.

## M2: Real inference and API hardening (Tue 10 Nov) -> Deploy D2
Goal: real predictions with safe input handling and tests. Until H1 delivers the real model, use the placeholder.

- [x] **T2.1 (MUST) Placeholder model.** Real production model `app/model/leaf.onnx` delivered from Kaggle training run; `app/model/MODEL_IS_DUMMY` removed. Commit: `chore: dev placeholder model`.
- [x] **T2.2 (MUST) inference.py.** Load the ONNX session once at import (CPUExecutionProvider). Functions: `preprocess(img) -> np.ndarray` (convert RGB, resize short side 256 bilinear, centre crop 224, /255, ImageNet mean/std, transpose(2,0,1), add batch axis, float32), `blur_score(img) -> float` (Laplacian variance on 256x256 grayscale), `predict(img, top_k=3) -> list[dict]` (stable softmax, argsort descending). `is_dummy()` returns whether `MODEL_IS_DUMMY` exists. Add short WHY comments (EXIF, float32, subtract max).
  Accept: `preprocess` returns shape (1,3,224,224), dtype float32; probabilities sum to 1. Commit: `feat: onnx inference pipeline`.
- [x] **T2.3 (MUST) API validation and bands.** Replace the fixed `/predict` with the real flow from the backend rules (8 MB -> 413; pixel cap and decode errors -> 400; `exif_transpose`; min side 100 -> 400; predict; status from bands; `blurry` flag). `/health` reports `model: "dummy"|"real"`. Use `advisory.get` once M3 exists; until then omit `advice` or return the minimal fallback. Constants at the top with a "tuned in M5" comment.
  Accept: all error cases return clear messages and never 500. Commit: `feat: validated predict endpoint`.
- [x] **T2.4 (MUST) Tests.** In `tests/`: text file renamed `.jpg` -> 400; 9 MB upload -> 413; 50x50 image -> 400; valid sample -> 200 with 3 `top` items summing to at most 1.0001; `lang=xx` falls back to `en`; blurry image (Gaussian blurred sample) sets `blurry` true; `preprocess` shape/dtype; if `tests/fixtures/preproc_reference.npy` exists, assert `np.allclose(preprocess(ref_image), ref, atol=1e-4)` (this proves app preprocessing equals training preprocessing); decompression-bomb test using a generated image above the pixel cap -> 400.
  Accept: `pytest -q` green. Commit: `test: predict endpoint and preprocessing`.
- [x] **T2.5 (MUST) Latency script** `scripts/measure_latency.py`: warm up once, run `predict` on a sample image 30 times, print mean, p95 and max in ms. Never write numbers into docs itself. Commit: `chore: latency script`.
- Agent: `/pre-deploy` for **D2**. **HUMAN: deploy D2** (`--allow-dummy` if the model is still a placeholder), tag `v0.6-api`.

## M3: Advisory knowledge base (Tue 10 to Wed 11 Nov)
Goal: the mechanism is built by the agent; the CONTENT is written by humans from approved sources.

- [x] **T3.1 (MUST) advisory.py.** `get(label, lang)` per the schema: returns title, symptoms, actions, prevention, source, disclaimer, reviewed flag for that language; unknown language falls back to `en`; missing label returns a safe fallback note ("No advisory available. Consult your local KVK or agriculture officer."). Also `display_name(label, lang)`. Commit: `feat: advisory lookup`.
- [x] **T3.2 (MUST) Skeleton generator** `scripts/make_advisory_skeleton.py`: reads `labels.json`, writes missing entries into `advisory.json` with `"<NEEDS ...>"` placeholders, never overwriting existing text, and fills `_disclaimer` en with the standard sentence "Indicative result only. Confirm with your local KVK before spraying." (hi and mr as `<NEEDS TRANSLATION>`). Commit: `feat: advisory skeleton generator`.
- [x] **T3.3 (MUST) Stricter checker.** Extend `scripts/check_advisory.py`: any value starting with `<NEEDS` counts as a problem; flag any string containing a dose-like pattern (digits followed by `ml`, `g/`, `kg/`, `l/`, `%`, `ppm`, `gm`) as `POSSIBLE DOSE` for human review; sources need name, url, retrieved date. Commit: `feat: stricter advisory checks`.
- [x] **T3.4 (MUST) Integrate.** `/predict` attaches `advice` for confident and uncertain results in the requested language and includes `name` per top item. Tests: advice present in `en`, `hi`, `mr`; absent when unrecognised. Commit: `feat: attach advice to predictions`.
- **HUMAN H3:** (1) run the skeleton generator; (2) write English entries from ICAR/state agricultural university/KVK sources in your own words, with title, link and retrieved date; NO chemical names or doses; (3) draft Hindi and Marathi, get a native speaker to correct them, then set `reviewed` to true per language; (4) `python scripts/check_advisory.py` must report 0 problems. The agent must not write or translate advice text.

## M4: Frontend (Wed 11 Nov) -> Deploy D3
Goal: a farmer-friendly phone UI. Follow `.agents/rules/20-frontend.md`.

- [x] **T4.1 (MUST) Layout and styling.** `static/index.html`, `styles.css`: screens Home, Result, History, About (one page, sections shown/hidden by JS); large buttons; high contrast; 360 px wide friendly; Noto Sans Devanagari from Google Fonts with fallbacks. Commit: `feat: ui layout`.
- [x] **T4.2 (MUST) Strings table.** One `STRINGS = {en:{...}, hi:{...}, mr:{...}}` object in `app.js` with every UI text key. Hindi and Marathi values start as `"<NEEDS TRANSLATION>"` shown in dev; humans fill them (H3). Language toggle persists in localStorage. Commit: `feat: i18n strings and toggle`.
- [x] **T4.3 (MUST) Upload flow.** Camera/gallery input, canvas shrink (640 px, JPEG 0.85, EXIF-aware), `fetch` to `/predict` with `lang`, spinner, error messages mapped to friendly text for 400/413/network failure. Commit: `feat: upload flow`.
- [x] **T4.4 (MUST) Result rendering.** Photo preview, disease name, confidence bar, status badge with TEXT (confident / uncertain / unrecognised), top-3 list, expandable symptoms / what to do now / prevention, source link, disclaimer, "translation under review" note when `reviewed` is false for the chosen language, Scan another. Unrecognised state shows retake guidance and no advice. Commit: `feat: result screen`.
- [x] **T4.5 (SHOULD) Photo tips and blur warning.** Show three tips on Home; show a warning banner when `blurry` is true. Commit: `feat: photo tips`.
- [x] **T4.6 (SHOULD) Voice read-aloud.** `speechSynthesis` with en-IN/hi-IN/mr-IN; check `getVoices()`; hide the button or show a tip if no matching voice; cancel on new speech. Commit: `feat: read aloud`.
- [x] **T4.7 (SHOULD) History.** Last 10 scans (label name, status, date) in localStorage with try/catch and a Clear button; text says nothing is stored on the server. Commit: `feat: local history`.
- [x] **T4.8 (SHOULD) About page.** How it works, dataset credits, supported crops list (generated from `labels.json` via a `/labels` endpoint or an inline list the human maintains), accuracy table with `<NOT MEASURED>` until the human fills it, known limits. Commit: `feat: about page`.
- [x] **T4.9 (COULD) PWA-lite.** `manifest.json` and icons only (no service worker unless asked). Commit: `feat: web manifest`.
- Agent: `/pre-deploy` for **D3** (real model required). **HUMAN: phone test on mobile data, deploy D3**, screenshots into `docs/evidence/` (strip metadata), tag `v0.8-ui`.

## M5: Field test, tuning, FEATURE FREEZE (Thu 12 Nov) -> Deploy D4
- [x] **T5.1 (MUST) Field evaluation script** `scripts/field_eval.py`: reads `tests/field_photos/<label>/*.jpg` (git-ignored), runs the same `inference.predict`, writes `field_results.csv` (file, true, predicted, prob, status) and prints accuracy, macro F1, top-3 accuracy and, per status band, how many answers were correct. Commit: `feat: field evaluation script`.
- [x] **T5.2 (MUST) Threshold sweep** `scripts/tune_thresholds.py`: reads `field_results.csv`, sweeps `CONF_OK` 0.5 to 0.9 and `CONF_LOW` 0.2 to 0.6, prints for each pair the share confident, accuracy among confident, and share unrecognised. It recommends nothing; humans choose. Commit: `feat: threshold sweep`.
- [x] **T5.3 (SHOULD) Failure log.** Script or section in `docs/TECH_NOTE.md` template listing misclassified files and the confusion pairs. Commit: `docs: failure analysis template`.
- [ ] **T5.4 (COULD) Occlusion heatmap** `scripts/occlusion.py` (offline script producing an image; no endpoint yet). Only if M0 to M5 MUSTs are done. Commit: `feat: occlusion script`.
- **HUMAN H5:** photograph 30 to 50 real leaves; run the scripts; choose thresholds (record reasons); update constants in `app/main.py`; fill TECH_NOTE numbers; set up an uptime monitor on `/health`; prepare the Render backup (manual) and a recorded fallback video; test on an older phone.
- Agent: `/pre-deploy` for **D4**. **HUMAN: deploy D4**, tag `v0.9-freeze`. FEATURE FREEZE: bug fixes only after this.

## M6: Submission pack (Fri 13 Nov) -> Deploy D5 only if needed
- [x] **T6.1 (MUST) README** with: problem, screenshots (from `docs/evidence/`), architecture diagram (Mermaid), run and test commands, dataset credits and licences, measured accuracy table (lab and field, only measured values), limitations, privacy statement ("photos are not stored"), live URL, and a link to `docs/DEPLOYMENTS.md`. Keep the Hugging Face front matter at the top. Commit: `docs: readme`.
- [x] **T6.2 (MUST) Tech note completion.** Fill structure from measured data supplied by humans; no invented values. Commit: `docs: tech note`.
- [ ] **T6.3 (MUST) Repo hygiene.** Check LICENSE choice (ask the human), `.gitignore`, no stray files, no TODO placeholders in shipped files, notebook outputs present and free of paths/names. Commit: `chore: repo hygiene`.
- **HUMAN H6:** slides, pitch video, native-speaker sign-off, two-person anonymity audit (repo, history, notebook, images, PDF, video). Run `/anonymity-audit`.
- Deploy **D5** only if README front matter or a bug fix changed shipped code. Tag `v1.0-rc`.

## M7: Final release (Sat 14 Nov, deploy before 12:00) -> Deploy D6
- [ ] **T7.1 (MUST) Final pre-deploy report** with `/pre-deploy` for D6 and a full end-to-end run on the live URL checklist (valid photo, text file, huge file, tiny file, blurry photo, 3 languages, voice, history).
- **HUMAN H7:** deploy D6, test on phone over mobile data, log in `docs/DEPLOYMENTS.md`, tag `v1.0-round1`, create the GitHub release with notes, submit, screenshot the confirmation.

## M8: Judging period (15 to 25 Nov)
- Critical fixes only: reproduce, fix on a branch, `/pre-deploy`, human deploys D7+. Never change the URL or Space name. Keep the uptime monitor green; open the app before each day.
