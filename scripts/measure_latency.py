"""Measure local CPU inference latency for LeafGuard.

Warms up the ONNX Runtime session once, then runs predict() 30 times on a sample image.
Reports mean, 95th percentile, and max latency in milliseconds.
Usage: python scripts/measure_latency.py
"""
import sys
import time
from pathlib import Path
import numpy as np
from PIL import Image

# Ensure project root is in sys.path when executed directly
ROOT_DIR = Path(__file__).resolve().parent.parent
if str(ROOT_DIR) not in sys.path:
    sys.path.insert(0, str(ROOT_DIR))

from app.inference import predict

SAMPLE_PATH = Path(__file__).resolve().parent.parent / "tests" / "sample_images" / "ref_leaf.jpg"


def main():
    if SAMPLE_PATH.exists():
        sample_img = Image.open(SAMPLE_PATH).convert("RGB")
    else:
        sample_img = Image.new("RGB", (400, 400), (80, 160, 90))

    # 1. Warm-up run (loads graph and initializes ONNX thread pools)
    print("Warming up ONNX Runtime engine...")
    _ = predict(sample_img)

    # 2. Benchmark 30 consecutive prediction runs
    num_runs = 30
    latencies_ms = []
    print(f"Running {num_runs} iterations on sample image...")

    for _ in range(num_runs):
        t0 = time.perf_counter()
        _ = predict(sample_img)
        dt_ms = (time.perf_counter() - t0) * 1000.0
        latencies_ms.append(dt_ms)

    # 3. Calculate statistics
    arr = np.array(latencies_ms)
    mean_ms = float(np.mean(arr))
    p95_ms = float(np.percentile(arr, 95))
    max_ms = float(np.max(arr))

    print("\n--- Latency Benchmark Results (CPU) ---")
    print(f"Iterations:     {num_runs}")
    print(f"Mean Latency:   {mean_ms:.2f} ms")
    print(f"p95 Latency:    {p95_ms:.2f} ms")
    print(f"Max Latency:    {max_ms:.2f} ms")
    print("---------------------------------------")


if __name__ == "__main__":
    main()
