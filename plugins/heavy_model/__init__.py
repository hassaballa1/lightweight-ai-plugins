from plugins._base import ModelFilePlugin


class HeavyModelPlugin(ModelFilePlugin):
    """High-accuracy, resource-hungry model (ONNX Runtime, GPU when available)."""

    name = "heavy"
    model_file = "heavy.onnx"
    runtime_module = "onnxruntime"

    def _load_real(self):
        import onnxruntime as ort
        providers = [p for p in ("CUDAExecutionProvider", "CoreMLExecutionProvider", "CPUExecutionProvider") if p in ort.get_available_providers()]
        return ort.InferenceSession(self.model_path, providers=providers)

    def _run_real(self, input_data):
        import numpy as np
        name = self.model.get_inputs()[0].name
        return self.model.run(None, {name: np.asarray(input_data, dtype=np.float32)})[0].tolist()


Plugin = HeavyModelPlugin
