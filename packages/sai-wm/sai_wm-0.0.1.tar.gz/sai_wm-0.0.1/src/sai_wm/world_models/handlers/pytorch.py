import numpy as np

IMPORT_ERROR_MESSAGE = (
    "PyTorch is not installed. Please install it using 'pip install torch'."
)

class PyTorchHandler:

    def __init__(self, models, device: str = "cpu"):
        try:
            import torch

            self._torch = torch
        except ImportError:
            raise ImportError(IMPORT_ERROR_MESSAGE)
        
        self.models = models
        self.device = device

        self._load_models()

    def _load_models(self):

        for (name, path) in self.models.items():

            self.models[name] = self._torch.jit.load(path, map_location=self._torch.device("cpu"))
            self.models[name].eval().to(self.device)

    def forward(self, input, name: str):
        input_tensor = self._to_torch(input)

        if isinstance(input_tensor, (tuple, list)):
            output = self.models[name](*input_tensor)
        else:
            output = self.models[name](input_tensor)

        return self._to_numpy(output)

    def categorical_sample(self, input):

        if not self._torch.is_tensor(input):
            input = self._torch.tensor(input, dtype=self._torch.float32)

        sample = self._torch.distributions.Categorical(input).sample()
        return sample.numpy()
    
    def normal_sample(self, mean, std):

        if not self._torch.is_tensor(mean):
            mean = self._torch.tensor(mean, dtype=self._torch.float32)

        if not self._torch.is_tensor(std):
            std = self._torch.tensor(std, dtype=self._torch.float32)

        sample = self._torch.distributions.Normal(mean, std).sample()
        return sample.numpy()

    def _to_torch(self, x):
        if isinstance(x, self._torch.Tensor):
            return x.to(self.device)

        if isinstance(x, np.ndarray):
            return self._torch.tensor(x, dtype=self._torch.float32, device=self.device)

        if isinstance(x, (float, int)):
            return self._torch.tensor([x], dtype=self._torch.float32, device=self.device)

        if isinstance(x, (list, tuple)):
            return type(x)(self._to_torch(v) for v in x)

        raise TypeError(f"Unsupported input type: {type(x)}")
    
    def _to_numpy(self, x):
        if isinstance(x, self._torch.Tensor):
            return x.detach().cpu().numpy()

        if isinstance(x, (list, tuple)):
            return type(x)(self._to_numpy(v) for v in x)

        # Already numpy / primitive? Just return
        return x
