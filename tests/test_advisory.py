"""Tests for advisory knowledge base lookup and multilingual integration."""
import io
import numpy as np
from PIL import Image
from fastapi.testclient import TestClient

from app.main import app
from app.advisory import get as get_advisory, display_name

client = TestClient(app)


def make_test_jpeg(width: int = 300, height: int = 300) -> bytes:
    img = Image.new("RGB", (width, height), color=(80, 160, 90))
    buf = io.BytesIO()
    img.save(buf, format="JPEG")
    return buf.getvalue()


def test_advisory_get_returns_required_schema():
    adv = get_advisory("Cotton___bacterial_blight", lang="en")
    assert "title" in adv
    assert "symptoms" in adv and isinstance(adv["symptoms"], list)
    assert "actions" in adv and isinstance(adv["actions"], list)
    assert "prevention" in adv and isinstance(adv["prevention"], list)
    assert "source" in adv and "name" in adv["source"] and "url" in adv["source"]
    assert "disclaimer" in adv
    assert "reviewed" in adv


def test_advisory_languages_supported():
    for lang in ("en", "hi", "mr"):
        adv = get_advisory("Cotton___healthy", lang=lang)
        assert adv["title"]
        assert adv["disclaimer"]


def test_advisory_unknown_lang_fallback():
    adv = get_advisory("Cotton___healthy", lang="klingon")
    assert adv["title"]
    assert adv["disclaimer"]


def test_display_name_formatting():
    name = display_name("Soybean___Soyabean_Mosaic", lang="en")
    assert "Soybean" in name or "Soyabean" in name


def test_predict_includes_advice_in_requested_lang():
    img_bytes = make_test_jpeg()
    for lang in ("en", "hi", "mr"):
        response = client.post(
            "/predict",
            files={"file": ("leaf.jpg", img_bytes, "image/jpeg")},
            data={"lang": lang},
        )
        assert response.status_code == 200
        data = response.json()
        if data["status"] != "unrecognised":
            assert "advice" in data
            assert data["advice"]["title"]
            assert data["advice"]["disclaimer"]


def test_predict_omits_advice_when_unrecognised():
    # Random noise image produces low, scattered probabilities (< 0.45)
    noise_arr = np.random.randint(0, 255, (300, 300, 3), dtype=np.uint8)
    img = Image.fromarray(noise_arr)
    buf = io.BytesIO()
    img.save(buf, format="JPEG")

    response = client.post(
        "/predict",
        files={"file": ("noise.jpg", buf.getvalue(), "image/jpeg")},
        data={"lang": "en"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "unrecognised"
    assert "advice" not in data
