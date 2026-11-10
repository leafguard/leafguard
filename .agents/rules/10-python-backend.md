---
activation: always_on
description: FastAPI and ONNX inference conventions
---
# Backend rules (FastAPI + ONNX Runtime)

## API contract
- `GET /health` returns `{"status":"ok","model":"real"}` (`"dummy"` when `app/model/MODEL_IS_DUMMY` exists). `GET /version` returns `{"sha","deployed_at","run_url"}` read from `app/version.json`, which exists only on the deployed copy (locally it returns sha `"dev"`).
- `POST /predict` is multipart: `file` (image) and `lang` (`en|hi|mr`, default `en`).
- Response JSON: `status` (`confident|uncertain|unrecognised`), `blurry` (bool), `top` (3 items of `label`,`prob`), and `advice` only when status is not `unrecognised`.
- Status bands are constants: `CONF_OK=0.70`, `CONF_LOW=0.45`, `BLUR_MIN=40.0`. They are TUNED on our own field photos and defined in one place only.

## Validation order in /predict (keep it)
1. Read bytes; reject over 8 MB with 413.
2. Set a safe `Image.MAX_IMAGE_PIXELS`; catch `Image.DecompressionBombError`, `UnidentifiedImageError`, `OSError` and return 400 with a plain message.
3. `img.load()`, then `ImageOps.exif_transpose(img)` (phone photos are stored sideways).
4. Reject if the shorter side is under 100 px with 400.
5. Predict, compute status, attach advice.
Errors use `HTTPException` with farmer-friendly text. Bad input must never produce a raw 500.

## Inference rules
- Load the ONNX session ONCE at import time, not per request. CPUExecutionProvider only.
- `preprocess()` mirrors training exactly: convert RGB, resize short side to 256 (bilinear), centre crop 224, divide by 255, ImageNet mean/std, transpose(2,0,1), add batch axis, float32.
- Softmax subtracts the max for numerical stability. `labels.json` order must equal the training class order.
- Never import torch or torchvision inside `app/`.

## Concurrency and privacy
- The app is stateless: no globals holding user data, no uploads written to disk, no database. Docs state plainly: photos are not stored.
- Do not log image bytes or filenames. Log only status, latency and error type.

## Tests (pytest + TestClient)
Keep tests for: `/health`, `/version`, text file renamed `.jpg` (400), oversized upload (413), tiny image (400), valid sample photo (200 with `top`), unknown `lang` falling back to `en`. Add a test whenever a bug is fixed.

## Do not
- Add CORS middleware (frontend is same-origin) unless the frontend moves.
- Generate advice with an LLM at runtime. Use `advisory.py` and `advisory.json` only.
