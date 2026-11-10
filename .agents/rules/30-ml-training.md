---
activation: model_decision
description: Use when editing training/ notebooks, exporting the model, or discussing metrics
---
# ML training and evaluation rules

- Training happens on Kaggle (Colab as backup), never on the laptop. Local code only loads `leaf.onnx`.
- Recipe: MobileNetV3-Large with ImageNet weights. Phase A: freeze backbone, AdamW lr 1e-3, about 3 epochs. Phase B: unfreeze, AdamW lr 1e-4, cosine schedule, about 6 epochs. Label smoothing 0.1, batch 64, 224x224. Augmentations: RandomResizedCrop(scale 0.5-1), flip, rotation 20, ColorJitter, RandomErasing(0.2).
- Augment training data only. Validation uses Resize(256) + CenterCrop(224).
- Set and print seeds (`random`, `numpy`, `torch`). Print library versions at the top of the notebook.
- PlantVillage has near-duplicate photos of the same leaf, so its validation score is optimistic. ALWAYS also evaluate on a separate field-style set (PlantDoc and our own phone photos) and report both.
- Record accuracy, macro F1, per-class recall, top-3 accuracy and a confusion matrix on BOTH sets. Keep them in the notebook output and `docs/TECH_NOTE.md`.
- Verify dataset coverage before promising a crop by listing class folders (PlantVillage soybean has only a healthy class).
- Export with `model.eval()`, opset 17, dynamic batch axis. Run the PyTorch vs ONNX parity check; the max difference must be about 1e-4 or smaller. Do not ship a model that fails parity.
- Never invent a metric. If it was not measured, write `<NOT MEASURED>`.
- Cite dataset licences and papers (PlantVillage, PlantDoc) in the README and tech note. Do not copy web images without permission.
