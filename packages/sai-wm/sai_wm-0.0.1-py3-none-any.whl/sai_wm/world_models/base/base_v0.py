import os
import json
import numpy as np
from huggingface_hub import hf_hub_download
from sai_wm.world_models.handlers import determine_model_type, get_handler

class BaseWM_v0:
    
    def __init__(self, 
                 world_config: dict, 
                 np_random: np.random.Generator,
                 device="cpu"):
        
        self.repo_id = world_config.get("repo_id", None)
        self.model_file = world_config.get("model_file", None)
        self.dream = world_config.get("dream", False)

        self.np_random = np_random
        
        self.device = device

        assert self.repo_id is not None and self.model_file is not None, (
            f"Repo ID must be specified to download the model files from HuggingFace"
        )

        self.cache_dir = os.path.expanduser("~/.cache/sai/world_models")
        os.makedirs(self.cache_dir, exist_ok=True)

        self._load_config()
        self._get_models()

        model_type = determine_model_type(list(self.models.values())[0])
        self.handler = get_handler(self.models, model_type)

    def _load_config(self):

        config_path = hf_hub_download(
            repo_id=self.repo_id,
            filename=f"{self.model_file}/config.json",
            local_dir=self.cache_dir
        )
        with open(config_path, "r") as f:
            self.config = json.load(f)
    
    def _get_models(self):

        self.models = {}
        for name, rel_path in self.config["components"].items():
            print(f"Loading {name} from {rel_path}")
            local_path = hf_hub_download(
                repo_id=self.repo_id,
                filename=f"{self.model_file}/{rel_path}",
                local_dir=self.cache_dir
            )
            self.models[name] = local_path
    
    def get(self, name):
        return self.models[name]
