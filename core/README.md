# core/

The `core` module is the control center of the framework. It handles:
- Plugin selection based on system resource usage
- Input routing to the correct AI plugin
- Execution flow and result collection

---

## Responsibilities

- Monitors system status (battery, CPU, etc.)
- Loads the correct plugin (light, medium, heavy)
- Executes the plugin’s prediction method
- Returns output to the main application

---

## Typical Files

| File            | Purpose                                |
|-----------------|----------------------------------------|
| `manager.py`    | Decision logic & plugin loader         |
| `runner.py`     | Orchestration of the AI call flow      |

