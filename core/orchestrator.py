from typing import Optional

from core.plugin_manager import load_plugin
from core.resource_selector import select_model_type
from interfaces.monitor_interface import SystemStatus
from interfaces.plugin_interface import PluginInterface
from utils.logger import get_logger

log = get_logger("orchestrator")


class Orchestrator:
    """Keeps one plugin loaded and swaps it when the selected tier changes."""

    def __init__(self):
        self.plugin: Optional[PluginInterface] = None

    def ensure_plugin(self, model_type: str) -> PluginInterface:
        if self.plugin is None or self.plugin.name != model_type:
            if self.plugin is not None:
                log.info("Swapping %s -> %s", self.plugin.name, model_type)
                self.plugin.unload_model()
            self.plugin = load_plugin(model_type)
            self.plugin.load_model()
        return self.plugin

    def reload(self):
        """Hot-reload the active plugin's code without restarting."""
        if self.plugin is not None:
            name = self.plugin.name
            self.plugin.unload_model()
            self.plugin = load_plugin(name, reload=True)
            self.plugin.load_model()

    def run(self, input_data, status: Optional[SystemStatus] = None):
        model_type = select_model_type(status)
        log.info("Selected model: %s", model_type)
        return self.ensure_plugin(model_type).run(input_data)


_default = Orchestrator()


def run_pipeline(input_data):
    return _default.run(input_data)
