# plugins/

This folder contains modular AI model plugins that follow a common interface.
Each plugin represents a different AI model based on its resource needs (light, medium, heavy).

---

## Structure

| Folder           | Description                                |
|------------------|--------------------------------------------|
| `light_model/`   | Lightweight AI model (fast, energy-efficient)  
| `medium_model/`  | Balanced AI model (moderate performance/cost)  
| `heavy_model/`   | High-performance model (accurate, resource-heavy)  

Each folder contains:
- `__init__.py`: Loads and runs the model
- `model_file.*`: Actual ML model (optional, stored separately)
- Any helper functions/classes

---

## Purpose

The system selects a plugin dynamically at runtime depending on the available system resources (CPU, battery, etc.).

---

## Interface Requirements

All plugin modules must implement these methods:

```python
def load_model():
    """Load and initialize the model."""
    pass

def predict(input_data):
    """Run inference and return the result."""
    return result