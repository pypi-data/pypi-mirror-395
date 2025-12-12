import numpy as np

IMPORT_ERROR_MESSAGE = (
    "Keras is not installed. Please install it using 'pip install tensorflow keras'."
)

class KerasHandler:

    def __init__(self, models, device: str = "cpu"):
        try:
            import tensorflow as tf
            import keras

            self._tf = tf
            self._keras = keras
            pass
        except ImportError:
            raise ImportError(IMPORT_ERROR_MESSAGE)
        
        self.models = models
        self.device = device

        self._load_models()

    def _load_models(self):

        for (name, path) in self.models.items():
            try:
                self.models[name] = self._keras.models.load_model(path)
            except Exception as e:
                raise RuntimeError(f"Failed to load Keras model '{name}' from {path}: {e}")

    def forward(self, input, name: str):
        input_tensor = self._to_tensor(input)

        if isinstance(input_tensor, (tuple, list)):
            output = self.models[name](*input_tensor)
        else:
            output = self.models[name](input_tensor)

        return self._to_numpy(output)

    def categorical_sample(self, input):

        logits = self._to_numpy(input)

        # Softmax to probabilities
        probs = self._softmax(logits)

        # Sample each batch independently
        samples = [np.random.choice(len(p), p=p) for p in probs]
        return np.array(samples, dtype=np.int64)
        
    def normal_sample(self, mean, std):

        mean = self._to_numpy(mean)
        std  = self._to_numpy(std)

        return np.random.normal(mean, std)
    
    def _softmax(self, x):
        x = np.asarray(x)
        e = np.exp(x - np.max(x, axis=-1, keepdims=True))
        return e / np.sum(e, axis=-1, keepdims=True)

    def _to_tensor(self, x):
        if isinstance(x, self._tf.Tensor):
            return x

        if isinstance(x, np.ndarray):
            return self._tf.convert_to_tensor(x, dtype=self._tf.float32)

        if isinstance(x, (float, int)):
            return self._tf.convert_to_tensor([x], dtype=self._tf.float32)

        if isinstance(x, (list, tuple)):
            return type(x)(self._to_tensor(v) for v in x)

        raise TypeError(f"Unsupported input type for KerasHandler: {type(x)}")
    
    def _to_numpy(self, x):
        if isinstance(x, self._tf.Tensor):
            return x.numpy()

        if isinstance(x, (list, tuple)):
            return type(x)(self._to_numpy(v) for v in x)

        # Already numpy / primitive? Just return
        return x
