"""Field evaluation script for LeafGuard (Task T5.1).

Evaluates the real ONNX model on a collection of real-world / field leaf photographs
stored under `tests/field_photos/<label>/*.jpg`.
Writes `field_results.csv` and prints Top-1 accuracy, Top-3 accuracy, Macro F1,
and per-band accuracy breakdown.
"""
import csv
import sys
from pathlib import Path
from collections import defaultdict

# Ensure repo root is on sys.path
REPO_ROOT = Path(__file__).resolve().parent.parent
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from PIL import Image
import numpy as np

from app.inference import predict
from app.main import CONF_OK, CONF_LOW


def compute_metrics(results):
    """Compute top-1 accuracy, top-3 accuracy, macro F1, and status band breakdown."""
    if not results:
        return

    total = len(results)
    correct_top1 = sum(1 for r in results if r["true"] == r["predicted"])
    correct_top3 = sum(1 for r in results if r["true"] in r["top3"])

    top1_acc = correct_top1 / total
    top3_acc = correct_top3 / total

    # Per-class counts for Macro F1
    classes = sorted(list({r["true"] for r in results} | {r["predicted"] for r in results}))
    tp = defaultdict(int)
    fp = defaultdict(int)
    fn = defaultdict(int)

    for r in results:
        t = r["true"]
        p = r["predicted"]
        if t == p:
            tp[t] += 1
        else:
            fn[t] += 1
            fp[p] += 1

    f1_list = []
    for c in classes:
        precision = tp[c] / (tp[c] + fp[c]) if (tp[c] + fp[c]) > 0 else 0.0
        recall = tp[c] / (tp[c] + fn[c]) if (tp[c] + fn[c]) > 0 else 0.0
        if precision + recall > 0:
            f1 = 2 * (precision * recall) / (precision + recall)
        else:
            f1 = 0.0
        f1_list.append(f1)

    macro_f1 = float(np.mean(f1_list)) if f1_list else 0.0

    # Per-status breakdown
    bands = {"confident": {"total": 0, "correct": 0},
             "uncertain": {"total": 0, "correct": 0},
             "unrecognised": {"total": 0, "correct": 0}}

    for r in results:
        status = r["status"]
        if status in bands:
            bands[status]["total"] += 1
            if r["true"] == r["predicted"]:
                bands[status]["correct"] += 1

    print("\n================ FIELD EVALUATION REPORT ================")
    print(f"Total field images evaluated: {total}")
    print(f"Top-1 Accuracy : {top1_acc * 100:.2f}% ({correct_top1}/{total})")
    print(f"Top-3 Accuracy : {top3_acc * 100:.2f}% ({correct_top3}/{total})")
    print(f"Macro F1 Score : {macro_f1:.4f}")
    print("---------------------------------------------------------")
    print("Status Band Breakdown:")
    for b_name, b_data in bands.items():
        b_tot = b_data["total"]
        b_corr = b_data["correct"]
        b_acc = (b_corr / b_tot * 100) if b_tot > 0 else 0.0
        pct_share = (b_tot / total * 100)
        print(f"  [{b_name.upper():12}] {b_tot:3d} images ({pct_share:5.1f}%) | "
              f"Correct: {b_corr:3d} | Band Accuracy: {b_acc:5.1f}%")
    print("=========================================================\n")


def main():
    root = Path(__file__).resolve().parent.parent
    field_dir = root / "tests" / "field_photos"
    out_csv = root / "field_results.csv"

    if not field_dir.exists():
        print(f"Field directory '{field_dir}' does not exist.")
        print("Create 'tests/field_photos/<label>/' and populate with test photos.")
        sys.exit(0)

    image_paths = []
    for ext in ("*.jpg", "*.jpeg", "*.png", "*.JPG", "*.JPEG", "*.PNG"):
        image_paths.extend(field_dir.glob(f"**/{ext}"))

    if not image_paths:
        print(f"No photos found in '{field_dir}'.")
        print("Place field photos in subdirectories named after class labels.")
        sys.exit(0)

    print(f"Found {len(image_paths)} field images in {field_dir}. Evaluating...")

    results = []
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["file", "true", "predicted", "prob", "status"])

        for img_path in sorted(image_paths):
            true_label = img_path.parent.name
            try:
                with Image.open(img_path) as img:
                    preds = predict(img, top_k=3)
            except Exception as e:
                print(f"Warning: Failed to process {img_path.name}: {e}")
                continue

            top_item = preds[0] if preds else {"label": "Unknown", "prob": 0.0}
            pred_label = top_item["label"]
            top_prob = top_item["prob"]
            top3_labels = [p["label"] for p in preds]

            if top_prob >= CONF_OK:
                status = "confident"
            elif top_prob >= CONF_LOW:
                status = "uncertain"
            else:
                status = "unrecognised"

            writer.writerow([str(img_path.name), true_label, pred_label, top_prob, status])
            results.append({
                "file": img_path.name,
                "true": true_label,
                "predicted": pred_label,
                "prob": top_prob,
                "status": status,
                "top3": top3_labels,
            })

    print(f"Wrote field results to {out_csv}")
    compute_metrics(results)


if __name__ == "__main__":
    main()
