"""FastAPI application for LeafGuard."""
from pathlib import Path
from fastapi import FastAPI, File, Form, UploadFile, HTTPException
from fastapi.staticfiles import StaticFiles

from app.version import get_version

# Threshold constants tuned on field photos (tune in M5)
CONF_OK = 0.70
CONF_LOW = 0.45
BLUR_MIN = 40.0

app = FastAPI(title="LeafGuard", description="Crop disease identification for smallholder farmers")

MODEL_DUMMY_MARKER = Path(__file__).parent / "model" / "MODEL_IS_DUMMY"


@app.get("/health")
def health() -> dict:
    """Return service health and whether real or dummy model is loaded."""
    model_type = "dummy" if MODEL_DUMMY_MARKER.exists() else "real"
    return {"status": "ok", "model": model_type}


@app.get("/version")
def version() -> dict:
    """Return deployed commit info or dev marker."""
    return get_version()


@app.post("/predict")
async def predict(file: UploadFile = File(...), lang: str = Form("en")) -> dict:
    """Stub prediction returning the fixed response in the final contract shape."""
    # Basic validation for skeleton
    contents = await file.read()
    if len(contents) > 8 * 1024 * 1024:
        raise HTTPException(status_code=413, detail="Image file too large (max 8 MB)")
    if len(contents) == 0:
        raise HTTPException(status_code=400, detail="Empty file uploaded")

    # Fixed skeleton response matching exact specification
    return {
        "status": "confident",
        "blurry": False,
        "top": [
            {"label": "Tomato___Late_blight", "name": "Tomato - Late blight", "prob": 0.93},
            {"label": "Tomato___Early_blight", "name": "Tomato - Early blight", "prob": 0.05},
            {"label": "Tomato___healthy", "name": "Tomato - Healthy", "prob": 0.01},
        ],
        "advice": {
            "title": "Tomato - Late blight",
            "symptoms": ["Dark water-soaked spots on leaves."],
            "actions": ["Remove and destroy infected leaves immediately."],
            "prevention": ["Avoid overhead watering, ensure good air circulation."],
            "source": {
                "name": "ICAR Extension Advisory",
                "url": "https://example.com/advisory",
                "retrieved": "2026-11-10",
            },
            "disclaimer": "Advice is for informational purposes only. Consult local KVK officer before applying treatments.",
            "reviewed": {"en": False, "hi": False, "mr": False},
        },
    }


# Mount static directory for frontend
STATIC_DIR = Path(__file__).resolve().parent.parent / "static"
STATIC_DIR.mkdir(parents=True, exist_ok=True)
app.mount("/", StaticFiles(directory=str(STATIC_DIR), html=True), name="static")
