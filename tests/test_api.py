import io
from fastapi.testclient import TestClient
from PIL import Image

from app.main import app

client = TestClient(app)


def make_dummy_jpeg(width: int = 200, height: int = 200) -> bytes:
    """Generate in-memory JPEG bytes for testing without external fixtures."""
    img = Image.new("RGB", (width, height), color=(80, 160, 90))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_health_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["model"] in ("dummy", "real")


def test_version_endpoint():
    response = client.get("/version")
    assert response.status_code == 200
    data = response.json()
    assert "sha" in data


def test_predict_endpoint_valid_image():
    img_bytes = make_dummy_jpeg()
    response = client.post(
        "/predict",
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("confident", "uncertain")
    assert "top" in data
    assert len(data["top"]) == 3
    assert "advice" in data


def test_predict_endpoint_with_matching_crop_filter():
    from pathlib import Path
    ref_path = Path(__file__).resolve().parent / "sample_images" / "ref_leaf.jpg"
    if ref_path.exists():
        with open(ref_path, "rb") as f:
            img_bytes = f.read()
    else:
        img_bytes = make_dummy_jpeg()

    response = client.post(
        "/predict",
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")},
        data={"lang": "en", "crop": "turmeric"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] in ("confident", "uncertain")
    assert len(data["top"]) <= 3
    turmeric_labels = {"Turmeric___Dry_Leaf", "Turmeric___Healthy_Leaf", "Turmeric___Leaf_Blotch"}
    for pred in data["top"]:
        assert pred["label"] in turmeric_labels


def test_predict_endpoint_rejects_crop_mismatch():
    from pathlib import Path
    ref_path = Path(__file__).resolve().parent / "sample_images" / "ref_leaf.jpg"
    if ref_path.exists():
        with open(ref_path, "rb") as f:
            img_bytes = f.read()
    else:
        img_bytes = make_dummy_jpeg()

    # Photograph of turmeric leaf sent with crop=soybean (deliberate mismatch)
    response = client.post(
        "/predict",
        files={"file": ("leaf.jpg", img_bytes, "image/jpeg")},
        data={"lang": "en", "crop": "soybean"},
    )
    assert response.status_code == 200
    data = response.json()
    # Mismatch must yield unrecognised status and low probability (no artificial boost)
    assert data["status"] == "unrecognised"
    assert data["top"][0]["prob"] < 0.20


def test_predict_rejects_oversized():
    huge_bytes = b"0" * (9 * 1024 * 1024)  # 9 MB
    response = client.post(
        "/predict",
        files={"file": ("huge.jpg", huge_bytes, "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 413


def test_predict_rejects_empty():
    response = client.post(
        "/predict",
        files={"file": ("empty.jpg", b"", "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 400

