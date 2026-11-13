"""Inference pipeline for LeafGuard using ONNX Runtime (CPU).

Preprocesses input images, runs MobileNetV3 ONNX graph, and calculates blur metrics.
No PyTorch dependency at serving time for fast startup and low memory footprint.
"""
from pathlib import Path
from typing import List, Dict, Any
import json
import numpy as np
from PIL import Image

import onnxruntime as ort

# Paths
BASE_DIR = Path(__file__).resolve().parent
MODEL_PATH = BASE_DIR / "model" / "leaf.onnx"
DUMMY_MARKER = BASE_DIR / "model" / "MODEL_IS_DUMMY"
LABELS_PATH = BASE_DIR / "data" / "labels.json"

# Load labels once at startup
with open(LABELS_PATH, "r", encoding="utf-8") as f:
    LABELS: List[str] = json.load(f)

# Load ONNX session once at module import (CPU Execution Provider)
_session: ort.InferenceSession = ort.InferenceSession(
    str(MODEL_PATH),
    providers=["CPUExecutionProvider"]
)
_input_name: str = _session.get_inputs()[0].name

# Standard ImageNet channel statistics used during training
IMAGENET_MEAN = np.array([0.485, 0.456, 0.406], dtype=np.float32)
IMAGENET_STD = np.array([0.229, 0.224, 0.225], dtype=np.float32)


def is_dummy() -> bool:
    """Return True if model is a development placeholder."""
    return DUMMY_MARKER.exists()


def preprocess(img: Image.Image) -> np.ndarray:
    """Transform image to normalized float32 tensor matching training exactly.

    Resize short side to 256 (bilinear), centre crop 224x224, scale / 255.0,
    normalize with ImageNet mean/std, transpose to (1, 3, 224, 224) float32.
    """
    # Force RGB mode (handles PNG alpha channels or grayscale uploads)
    img_rgb = img.convert("RGB")
    w, h = img_rgb.size

    # Resize shorter side to 256 maintaining aspect ratio
    if w < h:
        new_w = 256
        new_h = int(round(h * (256.0 / w)))
    else:
        new_h = 256
        new_w = int(round(w * (256.0 / h)))
    resized = img_rgb.resize((new_w, new_h), Image.Resampling.BILINEAR)

    # Centre crop to 224x224
    left = (new_w - 224) // 2
    top = (new_h - 224) // 2
    cropped = resized.crop((left, top, left + 224, top + 224))

    # Float32 conversion and [0, 1] scaling (matches torchvision.transforms.ToTensor)
    arr = np.array(cropped, dtype=np.float32) / 255.0

    # Channel normalization
    arr = (arr - IMAGENET_MEAN) / IMAGENET_STD

    # Transpose HWC -> CHW and add batch dimension NCHW -> (1, 3, 224, 224)
    tensor = np.expand_dims(arr.transpose(2, 0, 1), axis=0)
    return tensor.astype(np.float32)


CROP_FAMILY_MAP: Dict[str, List[str]] = {
    "cotton": [
        "Cotton___bacterial_blight",
        "Cotton___curl_virus",
        "Cotton___fussarium_wilt",
        "Cotton___healthy",
    ],
    "turmeric": [
        "Turmeric___Dry_Leaf",
        "Turmeric___Healthy_Leaf",
        "Turmeric___Leaf_Blotch",
    ],
    "soybean": [
        "Soybean___Healthy_Soyabean",
        "Soybean___Soyabean_Frog_Leaf_Eye",
        "Soybean___Soyabean_Mosaic",
        "Soybean___Soyabean_Spectoria_Brown_Spot",
    ],
    "tomato": [
        "Bacterial_Spot",
        "Early_Blight",
        "Healthy",
        "Late_Blight",
        "Septoria_Leaf_Spot",
        "Yellow_Leaf_Curl_Virus",
    ],
}


def blur_score(img: Image.Image) -> float:
    """Compute Laplacian variance on 256x256 grayscale to detect blurriness.

    Sharp images have high edge variance; blurred/unfocused leaves have low variance.
    """
    # Downsample to fixed 256x256 grayscale for fast, scale-invariant computation
    gray = img.convert("L").resize((256, 256), Image.Resampling.BILINEAR)
    arr = np.array(gray, dtype=np.float64)

    # 3x3 discrete Laplacian convolution kernel
    # [ 0,  1,  0]
    # [ 1, -4,  1]
    # [ 0,  1,  0]
    laplacian = (
        arr[0:-2, 1:-1]
        + arr[2:, 1:-1]
        + arr[1:-1, 0:-2]
        + arr[1:-1, 2:]
        - 4.0 * arr[1:-1, 1:-1]
    )
    return float(laplacian.var())


def predict(
    img: Image.Image,
    top_k: int = 3,
    crop: Optional[str] = None,
) -> List[Dict[str, Any]]:
    """Run model inference and return top-k predictions with calibrated probabilities.

    If crop is provided and matches a known crop family, probabilities are
    conditioned on that crop (Bayesian prior). Otherwise, global probabilities
    across all 27 classes are used.
    """
    tensor = preprocess(img)

    # Run ONNX model on CPU
    raw_outputs = _session.run(None, {_input_name: tensor})[0]
    logits = raw_outputs[0]

    # Stable Softmax: subtract maximum logit to avoid numerical overflow in exp()
    shift_logits = logits - np.max(logits)
    exp_logits = np.exp(shift_logits)
    probs = exp_logits / np.sum(exp_logits)

    crop_key = crop.lower().strip() if crop else "all"
    if crop_key in CROP_FAMILY_MAP:
        target_labels = set(CROP_FAMILY_MAP[crop_key])
        target_indices = [i for i, label in enumerate(LABELS) if label in target_labels]
        prob_sum = float(np.sum(probs[target_indices]))
        global_top_idx = int(np.argmax(probs))

        # Crop Mismatch Protection:
        # If a farmer selects Tomato by mistake but photographs Soybean, the total
        # evidence for the selected crop will be very low (< 15%) while another class dominates.
        # Do not artificially inflate to 50-70%; return uninflated raw probabilities so
        # confidence stays low (< 20%) and status is correctly marked 'unrecognised'.
        is_mismatch = (prob_sum < 0.15) and (global_top_idx not in target_indices)

        if prob_sum > 0 and not is_mismatch:
            cond_probs = {i: float(probs[i]) / prob_sum for i in target_indices}
            sorted_indices = sorted(target_indices, key=lambda i: cond_probs[i], reverse=True)[:top_k]
            results = []
            for idx in sorted_indices:
                results.append({
                    "label": LABELS[idx],
                    "prob": round(cond_probs[idx], 4),
                })
            return results
        elif is_mismatch:
            sorted_indices = sorted(target_indices, key=lambda i: probs[i], reverse=True)[:top_k]
            results = []
            for idx in sorted_indices:
                results.append({
                    "label": LABELS[idx],
                    "prob": round(float(probs[idx]), 4),
                })
            return results

    # Global top-k ranking over all 27 classes
    top_indices = np.argsort(probs)[::-1][:top_k]

    results = []
    for idx in top_indices:
        results.append({
            "label": LABELS[idx],
            "prob": round(float(probs[idx]), 4),
        })

    return results

