import importlib.util
import os

from interfaces.plugin_interface import PluginInterface
from utils.logger import get_logger

MODELS_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "models")


class ModelFilePlugin(PluginInterface):
    """Shared behaviour: load a real model if its runtime and file exist, else run a dummy."""

    runtime_module = ""  # e.g. "onnxruntime"

    def __init__(self):
        self.log = get_logger(f"plugin.{self.name}")
        self.model = None
        self.dummy = True

    @property
    def model_path(self) -> str:
        return os.path.join(MODELS_DIR, self.model_file)

    def load_model(self):
        has_file = os.path.isfile(self.model_path) and os.path.getsize(self.model_path) > 0
        has_runtime = importlib.util.find_spec(self.runtime_module) is not None
        if has_file and has_runtime:
            self.model = self._load_real()
            self.dummy = False
            self.log.info("Loaded %s with %s", self.model_file, self.runtime_module)
        else:
            reason = "model file empty/missing" if not has_file else f"{self.runtime_module} not installed"
            self.log.info("Loaded dummy %s model (%s)", self.name, reason)

    def run(self, input_data):
        if self.dummy:
            return self._dummy_run(input_data)
        return self._run_real(input_data)

    def unload_model(self):
        self.model = None
        self.dummy = True

    def _dummy_run(self, input_data):
        return {"model": self.name, "dummy": True, "output": f"[{self.name}] {input_data}"}

    def _load_real(self):
        raise NotImplementedError

    def _run_real(self, input_data):
        raise NotImplementedError
