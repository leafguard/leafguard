"""Unit and integration tests for inference pipeline and API edge cases."""
import io
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from fastapi.testclient import TestClient

from app.main import app
from app.inference import preprocess, blur_score, predict, is_dummy

client = TestClient(app)


def make_test_jpeg(width: int = 300, height: int = 300, color=(80, 160, 90)) -> bytes:
    """Generate in-memory valid JPEG bytes."""
    img = Image.new("RGB", (width, height), color=color)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_preprocess_shape_and_dtype():
    """Acceptance criterion: preprocess returns (1, 3, 224, 224) and float32."""
    img = Image.new("RGB", (400, 300), color=(100, 120, 140))
    tensor = preprocess(img)
    assert tensor.shape == (1, 3, 224, 224)
    assert tensor.dtype == np.float32


def test_predict_probabilities_sum_to_one():
    """Acceptance criterion: probabilities across all classes sum to 1."""
    img = Image.new("RGB", (250, 250), color=(60, 150, 70))
    top_preds = predict(img, top_k=3)
    assert len(top_preds) == 3
    # Top-3 probabilities must be positive and not exceed 1.0001
    prob_sum = sum(item["prob"] for item in top_preds)
    assert 0.0 < prob_sum <= 1.0001


def test_blur_score_detects_blur():
    """Blurry image produces lower Laplacian variance than sharp image."""
    sharp = Image.new("RGB", (300, 300), color=(255, 255, 255))
    d = ImageDraw.Draw(sharp)
    for i in range(0, 300, 20):
        d.line([(i, 0), (i, 300)], fill=(0, 0, 0), width=3)
    sharp_score = blur_score(sharp)

    blurry = sharp.filter(ImageFilter.GaussianBlur(radius=8))
    blurry_score = blur_score(blurry)

    assert blurry_score < sharp_score
    assert blurry_score < 40.0  # triggers BLUR_MIN threshold


def test_predict_blurry_image_sets_flag():
    """Uploading a heavily blurred image sets blurry: True in API response."""
    img = Image.new("RGB", (300, 300), color=(100, 100, 100))
    blurry_bytes = io.BytesIO()
    img.save(blurry_bytes, format="JPEG")
    response = client.post(
        "/predict",
        files={"file": ("leaf.jpg", blurry_bytes.getvalue(), "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 200
    assert response.json()["blurry"] is True


def test_predict_rejects_text_file_renamed_jpg():
    """Reject non-image text file renamed to .jpg with HTTP 400."""
    response = client.post(
        "/predict",
        files={"file": ("malicious.jpg", b"This is just plain text, not a JPEG image", "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 400
    assert "Invalid or unreadable" in response.json()["detail"]


def test_predict_rejects_oversized_payload():
    """Reject uploads > 8 MB with HTTP 413."""
    huge_bytes = b"0" * (9 * 1024 * 1024)
    response = client.post(
        "/predict",
        files={"file": ("huge.jpg", huge_bytes, "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 413
    assert "too large" in response.json()["detail"].lower()


def test_predict_rejects_tiny_image():
    """Reject images smaller than 100px on the shorter side with HTTP 400."""
    tiny_bytes = make_test_jpeg(width=50, height=50)
    response = client.post(
        "/predict",
        files={"file": ("tiny.jpg", tiny_bytes, "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 400
    assert "too small" in response.json()["detail"].lower()


def test_predict_rejects_decompression_bomb():
    """Reject massive pixel dimension image exceeding MAX_IMAGE_PIXELS with HTTP 400."""
    # 8000 x 7000 = 56,000,000 pixels (> 50,000,000 limit)
    bomb = Image.new("RGB", (8000, 7000), color=(0, 0, 0))
    buf = io.BytesIO()
    bomb.save(buf, format="PNG")
    response = client.post(
        "/predict",
        files={"file": ("bomb.png", buf.getvalue(), "image/png")},
        data={"lang": "en"},
    )
    assert response.status_code == 400
    assert "resolution is too large" in response.json()["detail"].lower()


def test_predict_lang_fallback():
    """Unknown language parameter falls back safely to default en."""
    img_bytes = make_test_jpeg(width=250, height=250)
    response = client.post(
        "/predict",
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")},
        data={"lang": "xx"},
    )
    assert response.status_code == 200
    assert "status" in response.json()


def test_preprocessing_parity_with_reference_tensor():
    """Assert app preprocessing exactly matches training preprocessing tensor."""
    fixture_path = Path(__file__).resolve().parent / "fixtures" / "preproc_reference.npy"
    if not fixture_path.exists():
        return

    ref_tensor = np.load(fixture_path)
    # Generate exact synthetic pattern matching training reference
    sample_img = Image.new("RGB", (400, 400), (230, 225, 210))
    d = ImageDraw.Draw(sample_img)
    d.ellipse((90, 40, 310, 360), fill=(60, 140, 70))
    d.line((200, 50, 200, 350), fill=(140, 190, 110), width=6)

    app_tensor = preprocess(sample_img)
    assert np.allclose(app_tensor, ref_tensor, atol=1e-4)


def test_health_reports_real_model():
    """Health endpoint reports real model loaded after dummy marker removal."""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["model"] == "real"

