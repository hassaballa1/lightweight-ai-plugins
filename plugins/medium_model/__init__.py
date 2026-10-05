from plugins._base import ModelFilePlugin


class MediumModelPlugin(ModelFilePlugin):
    """Balanced model (TensorFlow Lite)."""

    name = "medium"
    model_file = "medium.tflite"
    runtime_module = "tflite_runtime"

    def _load_real(self):
        from tflite_runtime.interpreter import Interpreter
        interpreter = Interpreter(model_path=self.model_path)
        interpreter.allocate_tensors()
        return interpreter

    def _run_real(self, input_data):
        import numpy as np
        inp = self.model.get_input_details()[0]
        out = self.model.get_output_details()[0]
        self.model.set_tensor(inp["index"], np.asarray(input_data, dtype=inp["dtype"]))
        self.model.invoke()
        return self.model.get_tensor(out["index"]).tolist()


Plugin = MediumModelPlugin
