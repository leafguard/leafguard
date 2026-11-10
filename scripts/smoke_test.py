"""Smoke test for a LIVE deployment.
Usage: BASE_URL=https://... [EXPECTED_SHA=...] [REQUIRE_REAL_MODEL=1] python scripts/smoke_test.py"""
import io, os, sys, time
import requests
from PIL import Image, ImageDraw

BASE = os.environ.get("BASE_URL", "http://localhost:8000").rstrip("/")
EXPECTED = os.environ.get("EXPECTED_SHA")
REQUIRE_REAL = os.environ.get("REQUIRE_REAL_MODEL", "0") == "1"
WAIT_S = int(os.environ.get("WAIT_SECONDS", "900"))  # a Space rebuild can take several minutes


def sample_jpeg() -> bytes:
    """Synthetic leaf-like image so the test needs no private photo."""
    img = Image.new("RGB", (400, 400), (230, 225, 210))
    d = ImageDraw.Draw(img)
    d.ellipse((90, 40, 310, 360), fill=(60, 140, 70))
    d.line((200, 50, 200, 350), fill=(140, 190, 110), width=6)
    buf = io.BytesIO(); img.save(buf, "JPEG"); return buf.getvalue()


def wait_for_commit() -> dict:
    deadline = time.time() + WAIT_S
    last = "no response"
    while time.time() < deadline:
        try:
            v = requests.get(f"{BASE}/version", timeout=15).json()
            last = v.get("sha")
            if not EXPECTED or v.get("sha") == EXPECTED:
                return v
        except Exception as e:  # Space still building or waking up
            last = type(e).__name__
        print(f"waiting for the new build... (live sha: {last})"); time.sleep(20)
    sys.exit(f"FAIL: live site did not report commit {EXPECTED} (last seen: {last})")


def check(name: str, ok: bool, detail: str = "") -> bool:
    print(("PASS  " if ok else "FAIL  ") + name + (f"  {detail}" if detail else "")); return ok


version = wait_for_commit()
results = [check("live commit matches", True, f"{str(version.get('sha'))[:7]} deployed {version.get('deployed_at')}")]
health = requests.get(f"{BASE}/health", timeout=15).json()
results.append(check("/health ok", health.get("status") == "ok", f"model={health.get('model')}"))
if REQUIRE_REAL:
    results.append(check("real model loaded (not dummy)", health.get("model") == "real"))
t0 = time.time()
r = requests.post(f"{BASE}/predict", files={"file": ("leaf.jpg", sample_jpeg(), "image/jpeg")}, data={"lang": "en"}, timeout=60)
ms = int((time.time() - t0) * 1000)
results.append(check("/predict valid image", r.status_code == 200 and "top" in r.json(), f"HTTP {r.status_code}, {ms} ms"))
r = requests.post(f"{BASE}/predict", files={"file": ("a.jpg", b"not an image", "image/jpeg")}, timeout=30)
results.append(check("/predict rejects non-image (400)", r.status_code == 400, f"HTTP {r.status_code}"))
r = requests.post(f"{BASE}/predict", files={"file": ("big.jpg", b"0" * (9 * 1024 * 1024), "image/jpeg")}, timeout=60)
results.append(check("/predict rejects oversize (413)", r.status_code == 413, f"HTTP {r.status_code}"))
print("RESULT:", "ALL PASSED" if all(results) else "FAILED")
sys.exit(0 if all(results) else 1)
