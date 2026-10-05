from abc import ABC, abstractmethod


class PluginInterface(ABC):
    """Contract every AI model plugin must implement."""

    name: str = "base"
    model_file: str = ""

    @abstractmethod
    def load_model(self):
        """Load the AI model into memory."""

    @abstractmethod
    def run(self, input_data):
        """Run inference and return the result."""

    def unload_model(self):
        """Release model resources. Optional."""
