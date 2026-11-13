# LeafGuard Technical Note

## 1. Problem and Scope
LeafGuard is an edge-optimized agricultural diagnostic system designed for smallholder farmers, with an emphasis on primary crops in Maharashtra and peninsular India, including:
- **Tomato, Potato, Pepper** (solanaceous crops)
- **Cotton** (*Gossypium* spp. — bacterial blight, leaf curl virus, wilt)
- **Turmeric** (*Curcuma longa* — leaf spot, leaf blotch, rhizome rot)
- **Soybean** (*Glycine max* — septoria brown spot, frogeye, bacterial blight)

Smallholder farmers often face diagnostic delays and lack immediate access to agricultural extension officers (KVKs). LeafGuard provides instantaneous top-3 differential diagnosis, image quality validation (blur detection), and verified ICAR/KVK management practices in English, Hindi, and Marathi, running entirely on low-cost CPU instances without cloud GPU dependencies.

---

## 2. Data and Licences
The model is trained on a combination of open agricultural research datasets:
- **PlantVillage Dataset**: Crowdsourced laboratory leaf images under controlled illumination (CC-BY 4.0 / Open Access).
- **Cotton Disease Datasets**: Public agronomic image collections covering major cotton pathogens.
- **Turmeric Leaf Disease Datasets**: Regional collections covering leaf spot and rhizome-associated foliar symptoms.
- **Soybean Disease Datasets**: Field collections covering foliar bacterial and fungal symptoms.
- **Field Test Set (`FIELD`)**: Uncurated mobile camera captures under variable sunlight, partial occlusions, and natural background clutter to evaluate real-world domain transfer.

> **Honest Note on Datasets**: Standard research datasets (such as PlantVillage) feature clean backgrounds with controlled lighting and near-duplicate leaves across classes. Validation scores on these datasets are optimistic. Real-world field accuracy must always be evaluated separately on uncurated mobile photographs.

---

## 3. Model Architecture and Training Pipeline
- **Backbone**: `MobileNetV3-Large` pretrained on ImageNet-1k. Chosen for its inverted residual blocks, squeeze-and-excitation attention, and minimal floating-point operation (FLOP) count for CPU execution.
- **Head**: Replaced final linear layer (`classifier[3]`) with `nn.Linear(in_features, num_classes)`.
- **Loss**: Cross-Entropy Loss with label smoothing ($\alpha = 0.1$) to prevent overconfident misclassifications on out-of-distribution inputs.
- **Two-Phase Transfer Learning**:
  - *Phase A (Warmup, 3 epochs)*: Backbone features frozen; classification head trained with `AdamW` ($\text{lr} = 10^{-3}$, weight decay $= 10^{-2}$).
  - *Phase B (Fine-tuning, 6 epochs)*: Entire network unfrozen; trained with `AdamW` ($\text{lr} = 10^{-4}$) and a Cosine Annealing learning rate schedule ($T_{\max} = 6$).
- **Augmentation**: `RandomResizedCrop(224, scale=(0.5, 1.0))`, `RandomHorizontalFlip`, `RandomRotation(20)`, `ColorJitter(0.3, 0.3, 0.3, 0.05)`, and `RandomErasing(p=0.2)`.

---

## 4. Evaluation and Results

*All values below reflect empirical evaluation. Placeholders mark metrics awaiting measurement from the Kaggle training run.*

| Metric | Laboratory Validation (Split) | Field Evaluation Set | Measurement Method |
|---|---|---|---|
| **Top-1 Accuracy** | 98.85% | `<NOT MEASURED>` | Multiclass accuracy |
| **Top-3 Accuracy** | 100.00% | `<NOT MEASURED>` | Target in top-3 highest logits |
| **Macro F1 Score** | 0.9669 | `<NOT MEASURED>` | Unweighted average F1 across classes |
| **Model Size** | 16.43 MB | `<NOT MEASURED>` | ONNX file size on disk (target < 25 MB) |
| **Parity Diff (PyTorch vs ONNX)** | 4.53e-06 | N/A | $\max |\text{PyTorch} - \text{ONNX}|$ on identical input (must be $< 10^{-3}$) |

---

## 5. Serving and Inference Architecture
- **Runtime**: ONNX Runtime (CPU Execution Provider) in Python 3.11 / FastAPI. PyTorch is excluded from the deployment container to keep image size small and boot times under 10 seconds.
- **Input Pipeline**:
  - Image decode using Pillow with decompressed pixel limit (`MAX_IMAGE_PIXELS = 50_000_000`) and 8 MB payload cap.
  - EXIF orientation normalization via `ImageOps.exif_transpose`.
  - Bilinear resize to shorter side 256 px, followed by center crop to $224 \times 224$ px.
  - Normalization: ImageNet channel mean $[0.485, 0.456, 0.406]$ and std $[0.229, 0.224, 0.225]$.
- **Quality Guardrails**:
  - **Blur Detection**: Laplacian variance computed on $256 \times 256$ grayscale conversion. Scores $< 40.0$ trigger a user warning flag.
  - **Confidence Bands**:
    - `confident` ($P \ge 0.70$): Diagnostic result and treatment advice displayed.
    - `uncertain` ($0.45 \le P < 0.70$): Result displayed with cautionary prompt to verify.
    - `unrecognised` ($P < 0.45$): Diagnosis withheld; advice omitted; user guided to retake photo.

---

## 6. Sourced Advisory Knowledge Base
- **Source Material**: Treatments, symptoms, and prevention recommendations are compiled strictly from Indian Council of Agricultural Research (ICAR), State Agricultural Universities (SAUs), and Krishi Vigyan Kendra (KVK) extension bulletins.
- **Safety Policy**: AI does not generate or extrapolate chemical dosages. Prescriptions strictly mention agronomic practices, cultural controls, and standard bio-pesticide guidelines; specific chemical applications carry mandatory disclaimers requiring local KVK officer confirmation.
- **Multilingual Support**: Stored key-value schema supporting English, Hindi, and Marathi, validated by native speakers.

---

## 7. Limitations and Known Failure Modes
1. **Domain Shift (Lab vs Field)**: Models trained on uniform grey/black backgrounds degrade when presented with direct soil background, harsh midday glare, or complex foliage.
2. **Multiple Pathogens / Co-infection**: Single-label classification does not isolate co-occurring nutritional deficiencies and fungal lesions on the same leaf.
3. **Out-of-Distribution Inputs**: Classifiers forced into softmax over plant classes can assign arbitrary predictions to non-leaf objects if confidence thresholds are not enforced.
4. **Early-stage vs Late-stage Symptoms**: Very early pinpoint lesions lack distinct geometric patterns and may fall into the `uncertain` band.

---

## 8. Reproducibility Guide
1. Open [training/train_kaggle.ipynb](file:///c:/Users/hp/Desktop/leafguard/training/train_kaggle.ipynb) in Kaggle Notebooks.
2. Attach dataset inputs (PlantVillage, Cotton, Turmeric, Soybean).
3. Set accelerator to GPU (NVIDIA T4 or P100).
4. Run all cells sequentially. The notebook generates:
   - `leaf.onnx`: Optimized graph (opset 17).
   - `labels.json`: Class index mapping.
   - `preproc_reference.npy`: Preprocessing reference tensor.
   - `metrics.json`: Full evaluation results.
5. Move generated artifacts to their corresponding local repository directories:
   - `leaf.onnx` $\to$ `app/model/leaf.onnx`
   - `labels.json` $\to$ `app/data/labels.json`
   - `preproc_reference.npy` $\to$ `tests/fixtures/preproc_reference.npy`
   - Metrics numbers $\to$ `docs/TECH_NOTE.md` and `docs/DEPLOYMENTS.md`.

---

## 9. Future Work
- Edge-device on-device inference via WebAssembly (ONNX Runtime Web) or TFLite to operate in zero-connectivity farming zones.
- Multi-crop segmentation mask prior to classification to isolate leaf boundaries from weeds and soil.
- Integration of seasonal weather advisory feeds via regional agromet services.

