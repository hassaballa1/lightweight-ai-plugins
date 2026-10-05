from plugins._base import ModelFilePlugin


class LightModelPlugin(ModelFilePlugin):
    """Fast, energy-efficient model (PyTorch / TorchScript)."""

    name = "light"
    model_file = "light.pt"
    runtime_module = "torch"

    def _load_real(self):
        import torch
        model = torch.jit.load(self.model_path, map_location="cpu")
        model.eval()
        return model

    def _run_real(self, input_data):
        import torch
        with torch.no_grad():
            return self.model(torch.as_tensor(input_data)).tolist()


Plugin = LightModelPlugin
