from gymnasium.utils.ezpickle import EzPickle

import gymnasium as gym
import numpy as np

from sai_wm.world_models.base.base_v0 import BaseWM_v0
from sai_wm.utils.v0.renderer import PygameRenderer

class BaseEnv_v0(gym.Env, EzPickle):

    metadata = {
        "render_modes": ["human", "rgb_array"],
        "render_fps": 30,
    }

    def __init__(self, 
                 env_config: dict, 
                 world_config: dict,
                 world_model_entry_points: dict,
                 **kwargs):
        
        super().__init__()
        self.env_config = env_config
        self.world_config = world_config
        self.render_mode = kwargs.get("render_mode", None)
        self.observation_space = None
        self.action_space = None

        self.use_base_env = env_config.get("use_base_env", True)
        self.dream = world_config.get("dream", True)

        self.wm_name = self.world_config["wm_name"]
        self.wm: BaseWM_v0 = self._load_world_model(world_model_entry_points[self.wm_name])

        self.initialize_renderer()

    def _get_info(self) -> dict:
        """
        Get additional information about the current state.

        This method can be overridden by subclasses to provide additional
        information that might be useful for debugging or logging.

        Returns:
            dict: Dictionary containing additional information
        """
        return {}
    
    def initialize_renderer(self):
        self.renderer = PygameRenderer()
    
    @staticmethod
    def _load_class(entry_point: str):
        """
        Load a class from its entry point string.

        Args:
            entry_point (str): The entry point string in the format 'module:ClassName'

        Returns:
            type: The loaded class
        """
        module_name, class_name = entry_point.rsplit(":", 1)
        module = __import__(module_name, fromlist=[class_name])
        return getattr(module, class_name)
    
    def _load_world_model(self, entry_point):

        world_model_class = self._load_class(entry_point)
        return world_model_class(self.world_config, self.np_random)
    
    def _get_obs(self) -> np.ndarray:
        """
        Get the complete observation for the current state.

        This method combines robot observations with environment-specific
        observations to form the complete observation vector.

        Returns:
            np.ndarray: Complete observation array
        """
        raise NotImplementedError
    
    def compute_terminated(self) -> bool:
        """
        Compute whether the episode has terminated.

        This method must be implemented by subclasses to define the termination
        conditions for the specific environment.

        Returns:
            bool: True if the episode should terminate, False otherwise

        Raises:
            NotImplementedError: If not implemented by subclass
        """
        raise NotImplementedError
    
    def render(self):
        """
        Render a frame from the MuJoCo simulation as specified by the render_mode.
        """
        
        if self.is_vectorized:
            frame = self.base_env.render().transpose(2, 0, 1)
            return self.renderer.render(frame, self.render_mode)

        if self.dream:
            return self.renderer.render(self.decoded, self.render_mode)
        else:
            return self.renderer.render(self.original, self.render_mode)

    def close(self):
        """Close rendering contexts processes."""
        if self.renderer is not None:
            self.renderer.close()