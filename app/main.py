"""FastAPI application for LeafGuard."""
import io
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles
from PIL import Image, ImageOps, UnidentifiedImageError

from app.version import get_version
from app.inference import predict as model_predict, blur_score, is_dummy
from app.advisory import get as get_advisory, display_name as get_display_name

# Threshold constants tuned on field photos (calibrated in M5)
CONF_OK = 0.40
CONF_LOW = 0.20
BLUR_MIN = 40.0

# Max decompressed image pixels to prevent decompression bombs (50 megapixels)
Image.MAX_IMAGE_PIXELS = 50_000_000

app = FastAPI(title="LeafGuard", description="Crop disease identification for smallholder farmers")


@app.get("/health")
def health() -> dict:
    """Return service health and whether real or dummy model is loaded."""
    model_type = "dummy" if is_dummy() else "real"
    return {"status": "ok", "model": model_type}


@app.get("/version")
def version() -> dict:
    """Return deployed commit info or dev marker."""
    return get_version()


@app.post("/predict")
async def predict(
    file: UploadFile = File(...),
    lang: str = Form("en"),
    crop: str = Form("all"),
) -> dict:
    """Validate image upload, execute ONNX inference, and return status bands."""
    # 1. Read bytes and enforce 8 MB payload limit (HTTP 413)
    contents = await file.read()
    if len(contents) > 8 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image file too large (max 8 MB)")
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    # 2. Decode image safely and catch image bombs or corrupt streams (HTTP 400)
    try:
        raw_img = Image.open(io.BytesIO(contents))
        if raw_img.width * raw_img.height > Image.MAX_IMAGE_PIXELS:
            raise HTTPException(status_code=400, detail="Image resolution is too large")
        raw_img.load()
    except HTTPException:
        raise
    except Image.DecompressionBombError:
        raise HTTPException(status_code=400, detail="Image resolution is too large")
    except (UnidentifiedImageError, OSError, ValueError):
        raise HTTPException(status_code=400, detail="Invalid or unreadable image file")

    # 3. EXIF normalization: mobile cameras save orientation metadata rather than rotating pixels
    try:
        img = ImageOps.exif_transpose(raw_img)
    except Exception:
        img = raw_img

    # 4. Reject tiny thumbnail images under 100 px on the shorter side
    w, h = img.size
    if min(w, h) < 100:
        raise HTTPException(status_code=400, detail="Image is too small (minimum side must be 100 pixels)")

    # 5. Measure blurriness using Laplacian variance
    blur_val = blur_score(img)
    is_blurry = blur_val < BLUR_MIN

    # 6. Execute ONNX model inference (crop-conditioned or global)
    top_preds = model_predict(img, top_k=3, crop=crop)
    for item in top_preds:
        item["name"] = get_display_name(item["label"], lang=lang)

    top_prob = top_preds[0]["prob"] if top_preds else 0.0

    # 7. Apply confidence status bands
    if top_prob >= CONF_OK:
        status = "confident"
    elif top_prob >= CONF_LOW:
        status = "uncertain"
    else:
        status = "unrecognised"

    response = {
        "status": status,
        "blurry": is_blurry,
        "top": top_preds,
    }

    # Advice contract: omitted when status is unrecognised; attached via advisory.get()
    if status != "unrecognised":
        top_label = top_preds[0]["label"]
        response["advice"] = get_advisory(top_label, lang=lang)

    return response


# Mount static directory for frontend
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
