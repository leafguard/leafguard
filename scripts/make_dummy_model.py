"""Development mock generator: builds a minimal ONNX model for CI and offline API testing.

Generates a lightweight graph so the API service and endpoints can be tested in isolation.
"""
import json, pathlib
import numpy as np
import onnx
from onnx import TensorProto, helper, numpy_helper

root = pathlib.Path(__file__).resolve().parent.parent
labels = json.loads((root / "app/data/labels.json").read_text(encoding="utf-8"))
n = len(labels)
w = numpy_helper.from_array((np.random.RandomState(0).randn(3, n) * 0.5).astype(np.float32), "W")
b = numpy_helper.from_array(np.zeros(n, dtype=np.float32), "B")
nodes = [helper.make_node("GlobalAveragePool", ["input"], ["gap"]),
         helper.make_node("Flatten", ["gap"], ["flat"], axis=1),
         helper.make_node("Gemm", ["flat", "W", "B"], ["logits"])]
graph = helper.make_graph(nodes, "dummy_leaf_model",
    [helper.make_tensor_value_info("input", TensorProto.FLOAT, ["batch", 3, 224, 224])],
    [helper.make_tensor_value_info("logits", TensorProto.FLOAT, ["batch", n])], [w, b])
model = helper.make_model(graph, opset_imports=[helper.make_opsetid("", 17)]); model.ir_version = 8
onnx.checker.check_model(model)
(root / "app/model").mkdir(parents=True, exist_ok=True)
onnx.save(model, str(root / "app/model/leaf.onnx"))
(root / "app/model/MODEL_IS_DUMMY").write_text("placeholder model; replace with the real Kaggle export\n")
print(f"dummy model written for {n} labels")
