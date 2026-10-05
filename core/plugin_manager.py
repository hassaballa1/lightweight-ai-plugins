import importlib
import pkgutil
import sys
from typing import Dict, Type

import plugins
from interfaces.plugin_interface import PluginInterface
from utils.logger import get_logger

log = get_logger("plugin_manager")


def discover_plugins() -> Dict[str, Type[PluginInterface]]:
    """Find every plugins/<name>_model package that exposes a `Plugin` class."""
    found = {}
    for info in pkgutil.iter_modules(plugins.__path__):
        if not info.ispkg:
            continue
        module = importlib.import_module(f"plugins.{info.name}")
        cls = getattr(module, "Plugin", None)
        if isinstance(cls, type) and issubclass(cls, PluginInterface):
            found[cls.name] = cls
    return found


def load_plugin(name: str, reload: bool = False) -> PluginInterface:
    """Instantiate a plugin by tier name. `reload=True` re-imports its code (hot-swap)."""
    module_name = f"plugins.{name}_model"
    if reload and module_name in sys.modules:
        importlib.reload(sys.modules[module_name])
        log.info("Reloaded %s", module_name)
    available = discover_plugins()
    if name not in available:
        raise ValueError(f"No plugin found for {name!r}; available: {sorted(available)}")
    return available[name]()
