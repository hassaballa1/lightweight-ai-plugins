# models/

This folder stores the actual **AI model files** used by the different plugin implementations.

Each plugin (light, medium, heavy) loads its corresponding model from here using a path or model loader.

---

## Structure Example

| Model Plugin       | File in `models/` Folder       |
|--------------------|-------------------------------|
| `light_model`      | `light_model.onnx` or `light_model.pt`  
| `medium_model`     | `medium_model.onnx`  
| `heavy_model`      | `heavy_model.pt`  

---

## Model Types You Can Use

| Format      | Framework           |
|-------------|---------------------|
| `.onnx`     | ONNX Runtime         |
| `.pt`       | PyTorch              |
| `.tflite`   | TensorFlow Lite (edge devices)  
| `.pkl`      | Sklearn or basic models  

---

## How Plugins Use These Models

Each plugin imports or loads the model like:

```python
import onnxruntime

def load_model():
    session = onnxruntime.InferenceSession("models/light_model.onnx")
    return session