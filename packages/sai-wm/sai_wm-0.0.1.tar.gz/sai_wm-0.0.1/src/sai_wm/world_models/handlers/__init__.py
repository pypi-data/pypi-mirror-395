import os

def determine_model_type(path: str) -> str:

    detected_model_type = False

    _, ext = os.path.splitext(path)
    ext = ext.lower()

    if ext in [".pt", ".pth"]:
        determined_model_type = "pytorch"
        detected_model_type = True

    # TensorFlow SavedModel or frozen graph
    elif ext in [".pb", ".pbx"]:
        determined_model_type = "tensorflow"
        detected_model_type = True

    # Keras HDF5 or native Keras format
    elif ext in [".h5", ".keras"]:
        determined_model_type = "keras"
        detected_model_type = True
    
    if detected_model_type is None:
        raise ValueError(
            f"Could not determine model type for object."
            f"Expected PyTorch, TensorFlow, or Keras model."
        )
    
    return determined_model_type

def get_handler(models_dict: dict, model_type: str):

    if model_type == "pytorch":
        from sai_wm.world_models.handlers.pytorch import PyTorchHandler
        handler = PyTorchHandler(models_dict)
    # elif model_type == "tensorflow":
    #     from sai_rl.model.handlers.tensorflow import TensorFlowModelHandler

    #     handler = TensorFlowModelHandler(env, console)
    # elif model_type == "keras":
    #     from sai_rl.model.handlers.keras import KerasModelHandler

    #     handler = KerasModelHandler(env, console)
    # else:
    #     raise ValueError(f"Unsupported model type: {model_type}")

    return handler

__all__ = ["determine_model_type", "get_handler"]
